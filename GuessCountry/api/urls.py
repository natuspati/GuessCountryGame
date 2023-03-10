from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from GuessCountry.api.views import (
    CountryListView, CountryDetailView, CountryViewSet, ScoreViewSet, UserDetailView,
)

# urlpatterns = [
#     path('countries/', CountryListView.as_view(), name='api_country_list'),
#     path('countries/<slug:slug>/', CountryDetailView.as_view(), name='api_country_detail')
# ]

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='api-country')
router.register(r'scores', ScoreViewSet, basename='api-score')
urlpatterns = router.urls

urlpatterns += [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token-auth/', views.obtain_auth_token),
    path('users/<str:email>', UserDetailView.as_view(), name='api-user-detail'),
]
