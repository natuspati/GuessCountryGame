from django.db import models
from django.core.validators import MinValueValidator
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

import uuid

from custom_auth.models import User


# Note table that contains comments on user scores or countries.
class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        formatted_date = self.modified_at.strftime('%Y-%m-%d%H:%M:%S')
        return 'Note: {} on {}'.format(self.content, formatted_date)


class Country(models.Model):
    REGIONS = (
        ('EU', 'Europe'),
        ('AS', 'Asia'),
        ('AM', 'Americas'),
        ('AF', 'Africa'),
        ('OC', 'Oceania'),
        ('AQ', 'Antarctic'),
    )
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=False)
    capital = models.CharField(max_length=100)
    region = models.CharField(max_length=100, choices=REGIONS)
    population = models.IntegerField(validators=[MinValueValidator(0)])
    flag = models.URLField(max_length=200)
    modified_at = models.DateTimeField(auto_now=True)
    notes = GenericRelation(Note)
    to_be_used_at = models.DateField(null=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        
        indexes = [
            models.Index(fields=['name'])
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('country-detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name


class Score(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    countries = models.ManyToManyField(Country, through='UserCountryRecord')
    value = models.PositiveIntegerField(default=0)
    notes = GenericRelation(Note)

    def __str__(self):
        return 'Score for {}: {}'.format(self.user.email, self.value)


class UserCountryRecord(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    user_score = models.ForeignKey(Score, on_delete=models.CASCADE)
    guessed = models.BooleanField(default=False, null=False, blank=False)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{} {} {} on {}'.format(
            self.user_score.user.email,
            'guessed' if self.guessed else 'did not guess',
            self.country.name,
            self.date.strftime('%Y-%m-%d%H:%M:%S')
        )
