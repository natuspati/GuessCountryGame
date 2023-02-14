from django.urls import path

from GuessCountry.views import IndexView, CountryListView, CountryDetailView, ScoreView, ScoreboardView

app_name = 'GuessCountry'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('country/', CountryListView.as_view(), name='country_list'),
    path('country/<slug:slug>/', CountryDetailView.as_view(), name='country_detail'),
    path('score/', ScoreView.as_view(), name='score'),
    path('scoreboard/', ScoreboardView.as_view(), name='scoreboard'),
]
