from django.db import models
from django.core.validators import MinValueValidator
from django.template.defaultfilters import slugify
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Note table that contains comments on user scores or countries.
class Note(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{} noted: {}".format(self.creator.name, self.content)


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
        return reverse('country_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name


class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)
    countries = models.ManyToManyField(Country)
    value = models.PositiveIntegerField(default=0)
    notes = GenericRelation(Note)
    
    def __str__(self):
        return f"{self.__class__.__name__} object for {self.user}"
