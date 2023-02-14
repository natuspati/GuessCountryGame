from django.views.generic import TemplateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from GuessCountry.models import Country

import random
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class IndexView(TemplateView):
    template_name = "GuessCountry/index.html"
    model = Country
    
    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        
        countries = list(Country.objects.all())
        context['country'] = random.choice(countries)
        
        logger.debug(f'Shown country: {context["country"].name}')
        return context


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# TODO: add argon password hashing
# TODO: add monthly scheduled task for PUT/PATCH requests
# TODO: add redis middleware to django apps
