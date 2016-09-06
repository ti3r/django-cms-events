from sekizai.context import SekizaiContext
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
import datetime

from models import EventListPlugin, EventRegistryPlugin, Event, EventRegistry

class EventList(CMSPluginBase):
    model = EventListPlugin
    name = _('Event list')
    render_template = 'cmsplugin_events/event_list_plugin.html'
    module = 'events'

    def render(self, context, instance, placeholder):
        object_list = Event.ongoing.all()
        if instance.category:
            object_list = object_list.filter(category=instance.category)
        uctx = SekizaiContext({'object_list': object_list,'instance': instance})
        return super(EventList,self).render(context, instance, placeholder)

plugin_pool.register_plugin(EventList)


class CalendarPlugin(CMSPluginBase):
    name = _('Events Calendar')
    render_template = 'cmsplugin_events/calendar.html'
    module = 'events'

    def render(self, context, instance, placeholder):
        uctx = SekizaiContext({'month':datetime.datetime.now().month})
        context.update(uctx)
        return super(CalendarPlugin,self).render(context,instance, placeholder)

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
            events = Event.ongoing.all()
            uctx = SekizaiContext({'events':events})
            context.update(uctx)

        return super(EventRegistrationPlugin, self).render(context, instance, placeholder)

plugin_pool.register_plugin(EventRegistrationPlugin)
