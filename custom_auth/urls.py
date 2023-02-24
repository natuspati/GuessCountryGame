from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView
from custom_auth.forms import CustomRegistrationForm


app_name = 'custom_auth'

urlpatterns = [
    path('accounts/register', RegistrationView.as_view(form_class=CustomRegistrationForm), name='register'),
]
