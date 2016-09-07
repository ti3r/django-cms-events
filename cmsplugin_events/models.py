from cms.models import CMSPlugin
from calendar import monthrange
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
import datetime
from filer.fields.image import FilerImageField
from django.core import urlresolvers


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class CurrentEventManager(models.Manager):
    def get_queryset(self):
        return super(CurrentEventManager, self).get_queryset().filter(
            event_end__gte=timezone.make_aware(
                datetime.datetime.now(), timezone.get_current_timezone()
            ))

class MonthEventManager(models.Manager):
    """
    Event manager to return the events ocurring in a specified month
    """

    def find(self, month=datetime.date.today().month):
        n = datetime.date.today()
        month_start = datetime.date(n.year, month, 1)
        range = monthrange(n.year, month)
        month_end = datetime.date(n.year, month, range[1])
        return super(MonthEventManager, self).get_queryset() \
            .filter(event_start__gte=month_start) \
            .filter(event_end__lte=month_end)


class CategoryEventManager(models.Manager):
    """
    Model manager for the Event class that will filter the results by a specified category
    """
    def find(self,category):
        return super(CategoryEventManager,self).get_queryset().filter(category=category)

class Event(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    description = models.TextField(_('Description'))
    event_start = models.DateTimeField(_('Start time'), null=True, blank=True)
    event_end = models.DateTimeField(_('End time'), null=True, blank=True)
    location = models.CharField(_('Location'), max_length=50, blank=True)
    image = FilerImageField(null=True, blank=True, default=None, verbose_name=_("Image"))
    category = models.ForeignKey(Category, null=True, blank=True)
    facebook_url = models.URLField(_('Facebook link'), blank=True)

    objects = models.Manager()
    ongoing = CurrentEventManager()
    month = MonthEventManager()
    by_category = CategoryEventManager()

    class Meta:
        ordering = ['event_start']

    @models.permalink
    def get_absolute_url(self):
        return 'event_details', (), {'pk': self.pk}

    def __unicode__(self):
        return self.title


class EventListPlugin(CMSPlugin):
    title = models.CharField(_('Title'), max_length=50)
    category = models.ForeignKey(Category, null=True, blank=True)

    def __unicode__(self):
        return self.category.name if self.category else _('All events')


class EventRegistry(models.Model):
    """
    Model to store one entry of the Events the registry
    """
    name = models.CharField(verbose_name=_('Full Name'), help_text=_('Name of the person to register'), null=False,
                            blank=False, max_length=512)
    email = models.EmailField(verbose_name=_('Email'), null=False, blank=False)
    event = models.ForeignKey(Event, null=False, blank=False)
    date = models.DateField(verbose_name=_('Registration Date'), help_text=_('Date of Registration'), null=False,
                            blank=False, default=timezone.now)

    objects = models.Manager()

    @classmethod
    def from_request(cls, request):
        n = request.POST['name']
        e = request.POST['email']
        ev = request.POST['event']
        event = Event.objects.get(id=ev)

        return EventRegistry.objects.create(name=n, email=e, event=event)


class EventRegistryPlugin(CMSPlugin):
    """
    Model class to store the configuration of the EventRegistrationPlugin plugin
    """
    title = models.CharField(verbose_name=_('Title'), help_text=_('Title to display on top of submission form'),
                             null=True, blank=True, max_length=512)
    message = models.CharField(verbose_name=_('Message'), help_text=_('Message to display after submit'), null=True,
                               blank=True, max_length=512)
    send_message = models.CharField(verbose_name=_('Submit Test'), help_text=_('Text to display in submit button'),
                                    null=True, blank=True, max_length=30)
    category_filter = models.ForeignKey(Category,null=True, blank=True, verbose_name=_('Categories Filter'),
                                        help_text=_('Only events in this category will be displayed as available for '
                                                    'registration'))
