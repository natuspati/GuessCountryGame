from django.urls import path

from GuessCountry.views import IndexView

app_name = 'GuessCountry'

urlpatterns = [
    path('', IndexView.as_view(), name="index")
]