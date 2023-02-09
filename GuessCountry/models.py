from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Region(models.Model):
    REGIONS = (
        ('EU', 'Europe'),
        ('AS', 'Asia'),
        ('AF', 'Africa'),
        ('OC', 'Oceania'),
        ('AQ', 'Antarctic'),
    )
    
    name = models.CharField(max_length=50, choices=REGIONS)
    
    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)
    capital = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    population = models.IntegerField(validators=[MinValueValidator(0)])
    flag = models.URLField(max_length=200)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        
        indexes = [
            models.Index(fields=['name'])
        ]
    
    def __str__(self):
        return self.name
