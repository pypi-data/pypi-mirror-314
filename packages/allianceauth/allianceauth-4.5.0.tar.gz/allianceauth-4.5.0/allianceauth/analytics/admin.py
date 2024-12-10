from django.contrib import admin

from .models import AnalyticsIdentifier, AnalyticsTokens


@admin.register(AnalyticsIdentifier)
class AnalyticsIdentifierAdmin(admin.ModelAdmin):
    search_fields = ['identifier', ]
    list_display = ('identifier',)


@admin.register(AnalyticsTokens)
class AnalyticsTokensAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ('name', 'type',)
