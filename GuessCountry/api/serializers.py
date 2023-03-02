from rest_framework import serializers

from GuessCountry.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'capital', 'region', 'population', 'flag']
