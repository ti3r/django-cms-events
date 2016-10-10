from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Event, Category, MonthEventManager
from django.core import serializers
from django.db.models import QuerySet

class EventListView(ListView):
    model = Event


class EventDetailView(DetailView):
    model = Event


class CategoryListView(ListView):
    model = Category


class EventsListInMonth(ListView):
    """
    List view to show the events in the current month or in a specific month as specified in the mth path variable
    """

    def get_queryset(self):
        if self.request.resolver_match.kwargs['mth']:
            month = self.request.resolver_match.kwargs['mth']
            queryset = Event.month.find(int(month))
        else:
            queryset = Event.month.find()

        return queryset


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
        if (m < 1 or m > 12):
            return HttpResponseBadRequest(content='{"error_code":1,"error_msg":"Month must be between 1 and 12"}',
                                          content_type='application/json')
        events = Event.month.find(m)
    else:
        events = Event.month.find()

    return HttpResponse(serializers.serialize('json', events), content_type='application/json')