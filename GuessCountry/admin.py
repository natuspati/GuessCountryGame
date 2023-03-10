from django.contrib import admin
from GuessCountry.models import Note, Country, Score, UserCountryRecord


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'capital')
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.
admin.site.register(Note)
admin.site.register(Country, CountryAdmin)
admin.site.register(Score)
admin.site.register(UserCountryRecord)
