from django.utils import timezone
from django.template.defaultfilters import truncatechars
from django.utils.html import strip_tags
from django.db import models
from tinymce.models import HTMLField


class Event(models.Model):
    name = models.CharField(max_length=256, blank=False)
    special = models.BooleanField(blank=False, default=False)
    begin_time = models.DateTimeField('Start', blank=False)
    end_time = models.DateTimeField('End', blank=False)
    description = HTMLField(blank=False)

    @property
    def status(self):
        now = timezone.localtime()
        if self.end_time < now:
            return 'done'
        elif self.begin_time > now:
            return 'scheduled'
        else:
            return 'ongoing'

    def __str__(self):
        date = timezone.localtime(self.begin_time).strftime('%d-%m-%Y')
        time = timezone.localtime(self.begin_time).strftime('%H:%M')
        return f'{self.name} ({date}, {time})'


class RoutineClass(models.Model):
    SUNDAY = 'Sunday'
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'

    WEEKDAY_CHOICES = [
        (SUNDAY, SUNDAY),
        (MONDAY, MONDAY),
        (TUESDAY, TUESDAY),
        (WEDNESDAY, WEDNESDAY),
        (THURSDAY, THURSDAY),
        (FRIDAY, FRIDAY),
        (SATURDAY, SATURDAY)
    ]

    name = models.CharField(max_length=256, blank=False)
    begin_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    weekday = models.CharField(max_length=10, choices=WEEKDAY_CHOICES, default=SUNDAY)

    @property
    def past_due(self):
        return self.end_time < timezone.localtime().time()

    def __str__(self):
        start = self.begin_time.strftime('%H:%M')
        end = self.end_time.strftime('%H:%M')
        return f'{self.name} - {self.weekday} ({start} - {end})'

    @property
    def start(self):
        return self.begin_time.strftime('%H:%M')

    @property
    def end(self):
        return self.end_time.strftime('%H:%M')


WEEKDAYS = (
        RoutineClass.MONDAY,
        RoutineClass.TUESDAY,
        RoutineClass.WEDNESDAY,
        RoutineClass.THURSDAY,
        RoutineClass.FRIDAY,
        RoutineClass.SATURDAY,
        RoutineClass.SUNDAY,
    )


class DefaultDescription(models.Model):
    event_name = models.CharField(max_length=256, unique=True, blank=False)
    description = HTMLField(blank=False)

    @property
    def short_description(self):
        desc = strip_tags(self.description)
        return truncatechars(desc, 32)

    def __str__(self):
        return f'{self.event_name}'
