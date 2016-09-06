from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Event, Category
from django.core import serializers

class EventListView(ListView):
    model = Event

class EventDetailView(DetailView):
    model = Event


class CategoryListView(ListView):
    model = Category


def events_registration_view(request):
    """
    View to handle the submission of a registration for an event
    :param request:
    :return:
    """
    return HttpResponse("OK")

def events_list_json_view(request):
    """
    Retrieves the list of events and serializes them as JSON object to be consumed asyncc
    :param request: If the request contains a parameter month (1-12) the events for the specified
    month will be returned
    :return: HttpResponse with the found entities serialized as json
    """
    events = None
    m = None
    if request.GET.get('month'):
        m = int(request.GET.get('month'))
        events = Event.month.find(m)
    else:
        events = Event.month.find()

    return HttpResponse(serializers.serialize('json', events), content_type='application/json')