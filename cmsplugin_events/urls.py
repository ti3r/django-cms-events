from django.conf.urls import patterns, url
from .views import EventListView, EventDetailView, events_list_json_view, events_registration_view

urlpatterns = patterns('',
    url(r'events$', EventListView.as_view(), name='events_list'),
    url(r'(?P<pk>\d+)/$', EventDetailView.as_view(), name='event_details'),
    url(r'events.json', events_list_json_view, name='events_list_json'),
    url(r'register$', events_registration_view, name='events_registration')
)
