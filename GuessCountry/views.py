from django.views.generic import TemplateView, ListView, DetailView, RedirectView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils import timezone

from GuessCountry.models import Country, Score
from GuessCountry.api.serializers import CountryShortSerializer

import random
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class IndexView(TemplateView):
    template_name = 'GuessCountry/index.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        # Set default values for new users
        request.session.setdefault('finished', False)
        request.session.setdefault('max_tries', settings.MAX_NUM_TRIES)
        request.session.setdefault('remaining_tries', settings.MAX_NUM_TRIES)
        request.session.setdefault('guessed_countries', [])
        
        # Select a country from database
        mystery_country = Country.objects.filter(to_be_used_at=timezone.now()).first()
        if not mystery_country:
            number_of_countries = Country.objects.count()
            random_idx = random.randrange(0, number_of_countries)
            mystery_country = Country.objects.all()[random_idx]
        
        # Check if previous country as the selected mystery country
        try:
            stored_country_id = request.session['country_data']['id']
            
            # User played the game today, load the previous state.
            if stored_country_id == mystery_country.pk:
                pass
            # Reset game if the user stored country is different from the selected mystery country.
            if stored_country_id != mystery_country.pk:
                request.session['finished'] = False
                request.session['remaining_tries'] = settings.MAX_NUM_TRIES
                request.session['guessed_countries'] = []
        except KeyError:
            pass
        
        context['progress_bar_width'] = int(request.session['remaining_tries'] / settings.MAX_NUM_TRIES * 100)
        request.session['country_data'] = CountryShortSerializer(mystery_country).data
        
        return self.render_to_response(context)


@method_decorator(cache_page(24 * 60 * 60), name='dispatch')
class CountryListView(ListView):
    model = Country
    queryset = Country.objects.order_by('name')
    context_object_name = 'country_list'
    template_name = 'GuessCountry/country_list.html'


@method_decorator(cache_page(24 * 60 * 60), name='dispatch')
class CountryDetailView(DetailView):
    model = Country
    template_name = 'GuessCountry/country_detail.html'


class ScoreView(TemplateView):
    template_name = 'GuessCountry/score_detail.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            user_score = Score.objects.get(user_id=request.user.id)
            context['score_value'] = user_score.value
        except ObjectDoesNotExist:
            context['score_value'] = 'No score'

        return self.render_to_response(context)


@method_decorator([cache_page(24 * 60 * 60), staff_member_required], name='dispatch')
class ScoreboardView(ListView):
    model = Score
    queryset = Score.objects.order_by('-value')
    context_object_name = 'score_list'
    template_name = 'GuessCountry/score_list.html'


class CountryCheckView(TemplateView):
    template_name = 'partials/country_check.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # If the game already completed, show the end state.
        if request.session['finished'] is True:
            context['country_name'] = request.session['country_data']['name']
        else:
            # Check if user has remaining tries.
            remaining_tries = request.session['remaining_tries']
            
            if remaining_tries > 0:
                guessed_country_name = request.GET['country_name']
                context['country_name'] = guessed_country_name.title()
                # Check if the guessed country is repeated.
                if context['country_name'] in request.session['guessed_countries']:
                    request.session['result'] = 'repeat'
                else:
                    mystery_country_id = request.session['country_data']['id']
                    guessed_country = Country.objects.filter(name__iexact=guessed_country_name).first()
                    
                    # Check if the input country exists in the database.
                    if not guessed_country:
                        request.session['result'] = 'skip'
                    else:
                        # Check if the input country and hidden country have the same primary key.
                        request.session['guessed_countries'].append(context['country_name'])
                        if guessed_country.pk == mystery_country_id:
                            request.session['result'] = 'success'
                            request.session['finished'] = True
                            
                            if request.user.is_authenticated:
                                user_score = Score.objects.filter(user_id=request.user.id).first()
                                user_score.value += 1
                                user_score.save()
                        else:
                            # Check if it is the last chance.
                            if remaining_tries == 1:
                                request.session['result'] = 'fail'
                                request.session['finished'] = True
                                context['country_name'] = request.session['country_data']['name']
                            else:
                                request.session['result'] = 'wait'
                            
                            request.session['remaining_tries'] -= 1
        
        context['result'] = request.session['result']
        context['remaining_tries'] = request.session['remaining_tries']
        context['progress_bar_width'] = int(request.session['remaining_tries'] / settings.MAX_NUM_TRIES * 100)
        return self.render_to_response(context)


class ResetSessionView(RedirectView):
    url = '/'
    query_string = False
    
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return super().get(request, *args, **kwargs)
