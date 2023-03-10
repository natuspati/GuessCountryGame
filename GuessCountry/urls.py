from django.urls import path, include

from GuessCountry.views import (
    IndexView, CountryListView, CountryDetailView, ScoreView, ScoreboardView, CountryCheckView, ResetSessionView
)

app_name = 'GuessCountry'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('country/all/', CountryListView.as_view(), name='country-list'),
    path('country/<slug:slug>/', CountryDetailView.as_view(), name='country-detail'),
    path('score/', ScoreView.as_view(), name='score'),
    path('scoreboard/', ScoreboardView.as_view(), name='scoreboard'),
    path('country_check', CountryCheckView.as_view(), name='country-check'),
    path('reset_session', ResetSessionView.as_view(), name='reset-session'),
    path('api/v1/', include('GuessCountry.api.urls')),
]
