from django.views.generic import TemplateView, ListView, DetailView

from GuessCountry.models import Country

import random


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
        return context


class CountryListView(ListView):
    model = Country
    queryset = Country.objects.order_by('name')
    context_object_name = 'country_list'
    template_name = 'GuessCountry/country_list.html'


class CountryDetailView(DetailView):
    model = Country
    template_name = 'GuessCountry/country_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# TODO: put info logger on get requests for country
# TODO: put critical logger on post requests (monthly updates)
# TODO: add monthly scheduled task for PUT/PATCH requests
# TODO: add redis middleware to django apps
