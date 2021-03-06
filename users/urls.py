from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from users.views import ClientDatatableView, ClientAdd, ClientUpdate, ClientDelete, ClientView
from users.views import UserProfileDatatableView, UserProfileAdd, UserProfileUpdate, UserProfileDelete
from users.views import UserProfileUpdatePassword, UserProfileView, CanceledClientAppointments
from users.views import ClientAppointmentsView, PendingClientAppointments

urlpatterns = [
    url(r'^$', login_required(ClientDatatableView.as_view()), name='list'),
    url(r'^add/$', login_required(ClientAdd.as_view()), name='add'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(ClientUpdate.as_view()), name='edit'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(ClientDelete.as_view()), name='delete'),
    url(r'^client/(?P<pk>\d+)/$', login_required(ClientView.as_view()), name='client'),
    url(r'^client-appointments/(?P<pk>\d+)/$', login_required(ClientAppointmentsView.as_view()), name='client_appointments'),
    url(r'^canceled-clients/$', login_required(CanceledClientAppointments.as_view()), name='clients_canceled'),
    url(r'^pending-clients/$', login_required(PendingClientAppointments.as_view()), name='clients_pending'),

    url(r'^staff/$', login_required(UserProfileDatatableView.as_view()), name='staff_list'),
    url(r'^staff/add/$', login_required(UserProfileAdd.as_view()), name='staff_add'),
    url(r'^staff/edit/(?P<pk>\d+)/$', login_required(UserProfileUpdate.as_view()), name='staff_edit'),
    url(r'^staff/edit-password/(?P<pk>\d+)/$', login_required(UserProfileUpdatePassword.as_view()), name='staff_edit_password'),
    url(r'^staff/delete/(?P<pk>\d+)/$', login_required(UserProfileDelete.as_view()), name='staff_delete'),
    url(r'^staff/view/(?P<pk>\d+)/$', login_required(UserProfileView.as_view()), name='staff'),
]
