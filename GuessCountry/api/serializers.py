from rest_framework import serializers
from django.utils.text import slugify

from GuessCountry.models import Country, Score, UserCountryRecord
from custom_auth.models import User
from GuessCountry.signals import daily_game_finished


class CountryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ['slug', 'modified_at', 'to_be_used_at']


class CountrySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False)
    
    class Meta:
        model = Country
        fields = '__all__'
        readonly = ['to_be_used_at']
    
    # Object-level validation in case slug is not provided.
    def validate(self, data):
        if not data.get('slug'):
            data['slug'] = slugify(data['name'])
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserCountryRecordSerializier(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    country_name = serializers.CharField(source='country.name')
    
    class Meta:
        model = UserCountryRecord
        fields = ['id', 'country_name', 'guessed', 'date', ]


class ScoreSerializer(serializers.ModelSerializer):
    countries = UserCountryRecordSerializier(source='usercountryrecord_set', many=True)
    
    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name='GuessCountry:api-user-detail',
        lookup_field='email'
    )
    
    class Meta:
        model = Score
        fields = '__all__'
    
    def update(self, instance, validated_data):
        countries = validated_data.pop('usercountryrecord_set')
        
        instance = super(ScoreSerializer, self).update(instance, validated_data)
        
        for country_data in countries:
            # Already existing countries won't have an id.
            if country_data.get('id'):
                continue
            # New country instance is spotted, check if it exists in database.
            try:
                new_country = Country.objects.get(name__iexact=country_data['country']['name'])
                daily_game_finished.send(
                    sender=''.format(self.__class__),
                    score=self.instance,
                    country=new_country,
                    success=country_data['guessed']
                )
            except Country.DoesNotExist:  # TODO: does not catch exception, raises AssertionError
                self.fail(f"Country {country_data['country']['name']} does not exist in database.")
        return instance
