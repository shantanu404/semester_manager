from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils import timezone
from django.db.models import Max

from .models import Event, RoutineClass, DefaultDescription, WEEKDAYS
import datetime


@admin.register(DefaultDescription)
class DefaultDescriptionsAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'short_description')
    search_fields = ('event_name',)


@admin.register(RoutineClass)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('name', 'weekday', 'start', 'end')
    list_filter = ('weekday', 'name')
    search_fields = ('name',)


def get_description(event_name):
    result = DefaultDescription.objects.filter(event_name=event_name)
    assert len(result) <= 1
    if len(result) == 0:
        return 'Please contact CR for link'
    return result[0].description


def generate_events(request):
    now = timezone.localtime()
    today = timezone.make_aware(datetime.datetime(day=now.day,
                                                  month=now.month,
                                                  year=now.year))

    one_day = datetime.timedelta(days=1)
    limit = today + datetime.timedelta(days=30)

    max_time = Event.objects.all().aggregate(Max('begin_time'))['begin_time__max']
    if max_time is not None:
        today = timezone.make_aware(datetime.datetime(day=max_time.day,
                                                      month=max_time.month,
                                                      year=max_time.year))
        today += one_day

    while today < limit:
        day_name = WEEKDAYS[today.weekday()]
        for lecture in RoutineClass.objects.filter(weekday=day_name):
            event_name = f'{lecture.name} Lecture'
            Event(name=event_name,
                  begin_time=today + datetime.timedelta(hours=lecture.begin_time.hour,
                                                        minutes=lecture.begin_time.minute,
                                                        seconds=lecture.begin_time.second),
                  end_time=today + datetime.timedelta(hours=lecture.end_time.hour,
                                                      minutes=lecture.end_time.minute,
                                                      seconds=lecture.end_time.second),
                  description=get_description(event_name)).save()
        today += one_day

    messages.success(request, f'Generated classes till {limit.strftime("%b %d, %Y")}')
    return HttpResponseRedirect('.')


class EventStatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('done', 'Done'),
            ('scheduled', 'Scheduled'),
            ('ongoing', 'Ongoing'),
        )

    def queryset(self, request, queryset):
        now = timezone.localtime()

        if self.value() == 'done':
            return queryset.filter(end_time__lt=now)
        elif self.value() == 'scheduled':
            return queryset.filter(begin_time__gt=now)
        elif self.value() == 'ongoing':
            return queryset.filter(begin_time__lt=now, end_time__gt=now)
        else:
            return queryset


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'begin_time', 'end_time', 'status')
    list_filter = ('begin_time', EventStatusFilter)
    search_fields = ('name',)
    list_per_page = 20
    ordering = ['begin_time']

    change_list_template = 'events/generate.html'

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path('generate', generate_events),
        ]
        return urls + extra_urls
