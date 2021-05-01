from django.shortcuts import render
from django.utils import timezone

from .models import Event, RoutineClass, WEEKDAYS


def index(request):
    now = timezone.localtime()
    events = Event.objects.filter(begin_time__day=now.day,
                                  begin_time__month=now.month,
                                  begin_time__year=now.year,
                                  begin_time__gte=now).order_by('begin_time')

    return render(request, 'events/events.html', {'events': events})


def routine(request):
    day_id = timezone.localtime().today().weekday()
    data = dict()
    for day in WEEKDAYS:
        data[day] = RoutineClass.objects.filter(weekday=day).order_by('begin_time')

    return render(request, 'events/routine.html', {'routine': data, 'weekday': WEEKDAYS[day_id]})

