from django.contrib import admin
from django.utils.html import format_html

from .models import AdoptionRequest

class AdoptionRequestAdmin(admin.ModelAdmin):
    readonly_fields = ["user", "cat"]
    list_display = ["__str__", "datetime", "status", "reason"]

    def get_ordering(self, request):
        return ["status"]

admin.site.register(AdoptionRequest, AdoptionRequestAdmin)