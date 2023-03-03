from rest_framework import serializers

from GuessCountry.models import Country


class CountryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'capital', 'region', 'population', 'flag']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
