from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from filer.fields.image import FilerImageField


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
                datetime.now(), timezone.get_current_timezone()
            ))


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

    class Meta:
        ordering = ['event_start']

    @models.permalink
    def get_absolute_url(self):
        return 'event_details', (), {'pk': self.pk}

    def __unicode__(self):
        return self.title

try:
    from cms.models import CMSPlugin
except ImportError:
    pass
else:
    class EventListPlugin(CMSPlugin):
        title = models.CharField(_('Title'), max_length=50)
        category = models.ForeignKey(Category, null=True, blank=True)

        def __unicode__(self):
            return self.category.name if self.category else _('All events')
