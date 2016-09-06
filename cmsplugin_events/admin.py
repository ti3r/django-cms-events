from django.contrib import admin
from .models import Event, Category, EventRegistry
from actions import export_csv

class EventAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('title', 'event_start', 'event_end', 'location', 'category')

class EventRegistryAdmin(admin.ModelAdmin):
    """
    Registry Admin View to check the registrations for a specific event
    """
    list_filter = ('event',)
    list_display = ('name','email','event', 'date',)
    actions = [export_csv]


admin.site.register(Category)
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistry, EventRegistryAdmin)