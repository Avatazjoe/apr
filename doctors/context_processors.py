from doctors.models import Doctor


def doctor_processor(request):
    return {'active_doctors': Doctor.objects.exclude(appointment=None)}