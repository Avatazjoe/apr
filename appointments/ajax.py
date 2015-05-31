import json
from datetime import datetime
from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext as _

from crispy_forms.utils import render_crispy_form
from jsonview.decorators import json_view
from schedule.models import Event
from schedule.periods import Period

from users.forms import AddClientForm, SelectClientForm
from appointments.forms import AppointmentForm, SimpleAppointmentForm, EventInfoForm, IDForm
from appointments.models import Appointment
from users.models import Client
from venues.models import Venue
from doctors.models import Doctor


def event_feed(request):
    if request.is_ajax() and request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                parser.parse(request.GET['start']), timezone.get_current_timezone())
            to = timezone.make_aware(
                parser.parse(request.GET['end']), timezone.get_current_timezone())
            period = Period(Event.objects.exclude(appointment=None).filter(
                appointment__customer=request.user.userprofile.customer), fro, to)
            occurences = [{'id': x.event.appointment_set.first().pk,
                           'title': "%s - %s - %s" % (x.event.appointment_set.first().client, x.event.appointment_set.first().client.client_id, x.title),
                           'className': 'event-info',
                           'start': timezone.localtime(x.start).isoformat(),
                           'end': timezone.localtime(x.end).isoformat(),
                           'resources': [x.event.appointment_set.first().venue.pk]
                           }
                          for x in period.get_occurrences()]
            breaks = [
                {
                    'start': 'T10:00:00',
                    'end': 'T10:30:00',
                    'dow': [0, 1, 2, 3, 4, 5, 6],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                },
                {
                    'start': 'T13:30:00',
                    'end': 'T14:30:00',
                    'dow': [0, 1, 2, 3, 4, 5, 6],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                }
            ]
        data = occurences + breaks
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


def venue_event_feed(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.is_ajax() and request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                parser.parse(request.GET['start']), timezone.get_current_timezone())
            to = timezone.make_aware(
                parser.parse(request.GET['end']), timezone.get_current_timezone())
            period = Period(
                Event.objects.exclude(appointment=None).filter(appointment__customer=request.user.userprofile.customer).filter(appointment__venue=venue), fro, to)
            occurences = [{'id': x.event.appointment_set.first().pk,
                           'title': "%s - %s - %s" % (x.event.appointment_set.first().client, x.event.appointment_set.first().client.client_id, x.title),
                           'className': 'event-info',
                           'start': timezone.localtime(x.start).isoformat(),
                           'end': timezone.localtime(x.end).isoformat(),
                           'resources': [x.event.appointment_set.first().venue.pk]
                           }
                          for x in period.get_occurrences()]
            breaks = [
                {
                    'start': 'T10:00:00',
                    'end': 'T10:30:00',
                    'dow': [0, 1, 2, 3, 4, 5, 6],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                },
                {
                    'start': 'T13:30:00',
                    'end': 'T14:30:00',
                    'dow': [0, 1, 2, 3, 4, 5, 6],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                }
            ]
        data = occurences + breaks
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


def doctor_event_feed(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.is_ajax() and request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                parser.parse(request.GET['start']), timezone.get_current_timezone())
            to = timezone.make_aware(
                parser.parse(request.GET['end']), timezone.get_current_timezone())
            period = Period(
                Event.objects.exclude(appointment=None).filter(appointment__customer=request.user.userprofile.customer).filter(appointment__doctor=doctor), fro, to)
            occurences = [{'id': x.event.appointment_set.first().pk,
                           'title': "%s - %s - %s" % (x.event.appointment_set.first().client, x.event.appointment_set.first().client.client_id, x.title),
                           'className': 'event-info',
                           'start': timezone.localtime(x.start).isoformat(),
                           'end': timezone.localtime(x.end).isoformat(),
                           'resources': [x.event.appointment_set.first().venue.pk]
                           }
                          for x in period.get_occurrences()]
            breaks = [
                {
                    'start': 'T10:00:00',
                    'end': 'T10:30:00',
                    'dow': [0, 1, 2, 3, 4, 5, 6],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                },
                {
                    'start': 'T13:30:00',
                    'end': 'T14:30:00',
                    'dow': [0, 1, 2, 3, 4, 5, 6],
                    'rendering': 'background',
                    'resources': [x.id for x in Venue.objects.all()]
                }
            ]
        data = occurences + breaks
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


@csrf_exempt
@json_view
def process_select_client_form(request):
    form = SelectClientForm(request.POST or None)
    form.fields['client'].queryset = Client.objects.filter(customer=request.user.userprofile.customer)
    if form.is_valid():
        return {
            'success': True,
            'client_id': form.cleaned_data['client'].id
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_add_client_form(request):
    form = AddClientForm(request.POST or None)
    if form.is_valid():
        client = form.create_client(request.user)
        return {
            'success': True,
            'client_id': client.id
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_edit_client_form(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = AddClientForm(request.POST or None, instance=client)
    if form.is_valid() and request.user.userprofile.customer == client.customer:
        form.save()
        return {
            'success': True,
            'client_id': client.id
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_edit_event_form(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventInfoForm(request.POST or None, instance=event)
    if form.is_valid() and request.user.userprofile.customer == event.appointment_set.first().customer:
        form.save()
        return {
            'success': True,
            'event_id': event.id
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}


@csrf_exempt
@json_view
def process_add_event_form(request):
    form = AppointmentForm(request.POST or None)
    form.fields['venue'].queryset = Venue.objects.filter(customer=request.user.userprofile.customer)
    if form.is_valid():
        form.create_appointment(request.user)
        messages.add_message(
            request, messages.SUCCESS, _('Successfully added appointment'))
        return {
            'success': True,
        }
    form_html = render_crispy_form(form)
    return {'success': False, 'form_html': form_html}

# NEW STYLE


def calendar_event_feed(request):
    if request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['start'])), timezone.get_current_timezone())
            to = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['end'])), timezone.get_current_timezone())
            period = Period(Event.objects.exclude(appointment=None).filter(
                appointment__customer=request.user.userprofile.customer), fro, to)
            data = [{'id': x.event.appointment_set.first().pk,
                     'title': "{}".format(x.event.appointment_set.first().client),
                     'userId': [x.event.appointment_set.first().venue.pk],
                     'start': x.start.isoformat(),
                     'end': x.end.isoformat(),
                     'clientId': x.event.appointment_set.first().client.pk,
                     'status': x.event.appointment_set.first().status
                     }
                    for x in period.get_occurrences()]
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


def printable_event_feed(request):
    if request.method == 'GET':
        if 'start' in request.GET and 'end' in request.GET:
            fro = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['start'])), timezone.get_current_timezone())
            to = timezone.make_aware(
                datetime.fromtimestamp(float(request.GET['end'])), timezone.get_current_timezone())
            period = Period(Event.objects.exclude(appointment=None).filter(
                appointment__customer=request.user.userprofile.customer), fro, to)
            data = [{'id': x.event.appointment_set.first().pk,
                     'title': "{} - {} - {}".format(x.event.appointment_set.first().client, x.event.appointment_set.first().client.client_id, x.title),
                     'userId': [x.event.appointment_set.first().venue.pk],
                     'start': x.start.isoformat(),
                     'end': x.end.isoformat(),
                     'clientId': x.event.appointment_set.first().client.pk
                     }
                    for x in period.get_occurrences()]
        return HttpResponse(json.dumps(data), content_type="application/json")
    # if all fails
    raise Http404


@login_required
def edit_event(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    success = False
    if request.user.userprofile.customer != appointment.customer:
        return False
    if request.is_ajax() and request.method == 'POST':
        form = SimpleAppointmentForm(request.POST)
        form.fields['venue'].queryset = Venue.objects.filter(customer=request.user.userprofile.customer)
        if form.is_valid():
            success = form.save_edit()
    return HttpResponse(json.dumps(success), content_type="application/json")


@login_required
def add_event(request):
    success = False
    print request.POST
    if request.is_ajax() and request.method == 'POST':
        form = SimpleAppointmentForm(request.POST)
        form.fields['venue'].queryset = Venue.objects.filter(customer=request.user.userprofile.customer)
        if form.is_valid():
            success = form.add_new(request.user)
    return HttpResponse(json.dumps(success), content_type="application/json")


@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    success = False
    if request.user.userprofile.customer != appointment.customer:
        return False
    if request.is_ajax() and request.method == 'POST':
        form = IDForm(request.POST)
        if form.is_valid() and form.cleaned_data['id'] == appointment.pk:
            appointment.delete()
            success = True
    return HttpResponse(json.dumps(success), content_type="application/json")


@login_required
def edit_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    success = False
    if request.user.userprofile.customer != appointment.customer:
        return False
    if request.is_ajax() and request.method == 'POST':
        form = IDForm(request.POST)
        if form.is_valid() and form.cleaned_data['id'] == appointment.pk:
            if 'status' in request.POST and request.POST['status'] in Appointment.STATUS_LIST:
                appointment.status = request.POST['status']
                appointment.save()
                success = True
    return HttpResponse(json.dumps(success), content_type="application/json")
