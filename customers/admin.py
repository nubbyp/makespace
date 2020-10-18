from django.contrib import admin
from .models import Plan

class PlanAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'storage_plan', 'start_date', 'end_date')
    fields = ('user_id', 'storage_plan', 'start_date', 'end_date')

admin.site.register(Plan, PlanAdmin)