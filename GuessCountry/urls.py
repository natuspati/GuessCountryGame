from django.urls import path

from GuessCountry.views import IndexView, CountryListView, CountryDetailView

app_name = 'GuessCountry'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('country/', CountryListView.as_view(), name='country_list'),
    path('country/<slug:slug>/', CountryDetailView.as_view(), name='country_detail'),
]