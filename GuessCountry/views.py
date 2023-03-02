from django.views.generic import TemplateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils import timezone

from GuessCountry.models import Country, Score
from GuessCountry.api.serializers import CountrySerializer

import random
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class IndexView(TemplateView):
    template_name = 'GuessCountry/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Select a mystery country for today, if there's none, pick a random country
        today = timezone.now()
        mystery_country = Country.objects.filter(to_be_used_at=today).first()
        if mystery_country:
            context['country'] = mystery_country
        else:
            number_of_countries = Country.objects.count()
            random_idx = random.randrange(0, number_of_countries)
            context['country'] = Country.objects.all()[random_idx]
        
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Enable this options in productions instead
        # request.session.setdefault('num_tries', 0)
        # request.session.setdefault('finished', False)
        request.session['num_tries'] = 0
        request.session['finished'] = False
        
        # Keep country information in session
        request.session['country_data'] = CountrySerializer(context['country']).data
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


@method_decorator([cache_page(3600), vary_on_cookie, login_required], name='dispatch')
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
        # Check if user has remaining tries.
        if request.session['num_tries'] <= settings.MAX_NUM_TRIES:
            guessed_country_name = request.GET['country_name']
            mystery_country_pk = int(request.GET['mystery_country_pk'])
            guessed_country = Country.objects.filter(name__iexact=guessed_country_name).first()
            # Check if the input country exists in the database.
            if guessed_country:
                # Check if the input country and hidden country have the same primary key.
                if guessed_country.pk == mystery_country_pk:
                    context['result'] = 'Correct! The answer is {}'.format(guessed_country.name)
                    request.session['finished'] = True
                    request.session['num_tries'] = 4
                else:
                    context['result'] = 'Incorrect!'
                    request.session['num_tries'] += 1
            else:
                context['result'] = 'Country {} does not exist!'.format(guessed_country_name)
        # If number of tries exceeded, disable input form.
        else:
            context['result'] = 'You are out of tries!'
            request.session['finished'] = True
            request.session['num_tries'] = 4
        return self.render_to_response(context)
