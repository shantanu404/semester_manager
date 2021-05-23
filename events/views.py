import datetime

from django.shortcuts import render
from django.utils import timezone

from .models import Event, RoutineClass, WEEKDAYS


def index(request):
    now = timezone.localtime()
    today = timezone.make_aware(datetime.datetime(day=now.day,
                                                  month=now.month,
                                                  year=now.year))

    events = Event.objects.filter(begin_time__day=now.day,
                                  begin_time__month=now.month,
                                  begin_time__year=now.year,
                                  end_time__gte=now).order_by('begin_time')

    special_events = Event.objects.filter(special=True, end_time__gte=now).order_by('begin_time')

    tomorrow = today + datetime.timedelta(days=1)

    upcoming_events = Event.objects.filter(begin_time__gte=tomorrow)\
                                   .order_by('begin_time')[:10]

    return render(request, 'events/events.html', {'events': events,
                                                  'special_events': special_events,
                                                  'upcoming_events': upcoming_events,
                                                  })


def routine(request):
    day_id = timezone.localtime().today().weekday()
    data = dict()
    for day in WEEKDAYS:
        data[day] = RoutineClass.objects.filter(weekday=day).order_by('begin_time')

    return render(request, 'events/routine.html', {'routine': data, 'weekday': WEEKDAYS[day_id]})

