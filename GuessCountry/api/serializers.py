from rest_framework import serializers
from django.utils.text import slugify

from GuessCountry.models import Country, Score


class CountryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ['slug', 'modified_at', 'to_be_used_at']


class CountrySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False)
    
    class Meta:
        model = Country
        fields = '__all__'
        readonly = ['modified_at', 'to_be_used_at']
    
    # Object-level validation in case slug is not provided.
    def validate(self, data):
        if not data.get('slug'):
            data['slug'] = slugify(data['name'])
        return data


class ScoreSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = Score
        fields = '__all__'

        # readonly = ['modified_at', 'created_at', 'user', 'user_email']
        