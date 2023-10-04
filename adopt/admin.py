from django.contrib import admin
from django.utils.html import format_html

from .models import AdoptionRequest

class AdoptionRequestAdmin(admin.ModelAdmin):
    readonly_fields = ["user", "cat"]

admin.site.register(AdoptionRequest, AdoptionRequestAdmin)