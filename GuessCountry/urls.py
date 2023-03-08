from django.urls import path, include

from GuessCountry.views import (
    IndexView, CountryListView, CountryDetailView, ScoreView, ScoreboardView, CountryCheckView, ResetSessionView
)

app_name = 'GuessCountry'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path(r'country/all/', CountryListView.as_view(), name='country-list'),
    path(r'country/<slug:slug>/', CountryDetailView.as_view(), name='country-detail'),
    path(r'score/', ScoreView.as_view(), name='score'),
    path(r'scoreboard/', ScoreboardView.as_view(), name='scoreboard'),
    path(r'country_check', CountryCheckView.as_view(), name='country-check'),
    path(r'reset_session', ResetSessionView.as_view(), name='reset-session'),
    path('api/v1/', include('GuessCountry.api.urls')),
]
