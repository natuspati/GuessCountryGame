from rest_framework import generics
from rest_framework import viewsets

from GuessCountry.models import Country, Score
from GuessCountry.api.serializers import CountrySerializer, ScoreSerializer, UserSerializer, LinkedScoreSerializer
from GuessCountry.api.permissions import ScoreUserModifyOrReadOnly, IsAdminUserForObject
from custom_auth.models import User


class CountryListView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'slug'


# Work with view sets for now
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'slug'


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [ScoreUserModifyOrReadOnly | IsAdminUserForObject]
    lookup_field = 'uuid'
    
    # Disallow post for creating new scores.
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"
