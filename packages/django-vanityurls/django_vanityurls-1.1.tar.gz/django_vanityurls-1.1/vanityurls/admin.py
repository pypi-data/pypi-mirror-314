from django.contrib import admin

from .models import VanityUrl

@admin.register(VanityUrl)
class VanityUrlAdmin(admin.ModelAdmin):

    list_display = ['vanity_url', 'target']
