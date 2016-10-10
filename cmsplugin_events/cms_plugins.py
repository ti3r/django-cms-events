from sekizai.context import SekizaiContext
from django.utils.translation import ugettext as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
import datetime
import calendar
from models import EventListPlugin, EventRegistryPlugin, Event, EventRegistry


class EventList(CMSPluginBase):
    """
    Plugin Class to render the list of ongoing events
    """
    model = EventListPlugin
    name = _('Event list')
    render_template = 'cmsplugin_events/event_list_plugin.html'
    module = 'events'

    def render(self, context, instance, placeholder):
        object_list = Event.ongoing.all()
        if instance.category:
            object_list = object_list.filter(category=instance.category)
        context.update({'object_list': object_list,'instance': instance})
        return super(EventList,self).render(context, instance, placeholder)

plugin_pool.register_plugin(EventList)


class CalendarPlugin(CMSPluginBase):
    name = _('Events Calendar')
    render_template = 'cmsplugin_events/calendar.html'
    module = 'events'
    cache = False

    def render(self, context, instance, placeholder):
        current_month = datetime.datetime.now().month
        events = Event.month.find(current_month)
        month_name = self.get_month_name(current_month)
        year = datetime.datetime.now().year
        #Tue is 1 monday is 7
        date_range = calendar.monthrange(year, current_month)
        uctx = SekizaiContext({'month':current_month,'month_name':month_name, 'year': year
                                ,'first_day_of_week':date_range[0], 'number_of_days_in_month': 'X'*date_range[1]
                                  ,'events':events})

        context.update(uctx)
        return super(CalendarPlugin,self).render(context,instance, placeholder)


    def get_month_name(self, month):
        if month == 1: return _('January')
        elif month == 2: return _('February')
        elif month == 3: return _('March')
        elif month == 4: return _('April')
        elif month == 5: return _('May')
        elif month == 6: return _('June')
        elif month == 7: return _('July')
        elif month == 8: return _('August')
        elif month == 9: return _('September')
        elif month == 10: return _('October')
        elif month == 11: return _('November')
        elif month == 12: return _('December')
        else: return _('Unknown Month')

plugin_pool.register_plugin(CalendarPlugin)


class EventRegistrationPlugin(CMSPluginBase):
    model = EventRegistryPlugin
    name = _('Event Registration Form')
    render_template = 'cmsplugin_events/register.html'
    module = 'events'

    def render(self, context, instance, placeholder):
        request = context['request']
        if request.method == 'POST' and "cmsplugin_events_register_" + str(instance.id) in request.POST.keys() :
            EventRegistry.from_request(request)
            context.update({'submitted':True})
        else:
            events = None
            if instance.current_month_filter:
                if instance.category_filter:
                    events = Event.month.find_by_category(instance.category_filter)
                else:
                    events = Event.month.find()
            elif instance.month_filter:
                if instance.category_filter:
                    events = Event.month.find_by_category(instance.category_filter,instance.month_filter)
                else:
                    events = Event.month.find(instance.month_filter)
            elif instance.category_filter:
                events = Event.by_category.find(instance.category_filter)
            else:
                events = Event.ongoing.all()
            uctx = SekizaiContext({'events':events})
            context.update(uctx)

        return super(EventRegistrationPlugin, self).render(context, instance, placeholder)

plugin_pool.register_plugin(EventRegistrationPlugin)
