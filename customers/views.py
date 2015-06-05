from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from customers.mixins import CustomerMixin
from customers.forms import NewCustomerForm, CustomerForm
from subscriptions.models import Subscription


class NewCustomer(FormView):
    template_name = 'customers/new.html'
    form_class = NewCustomerForm
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super(NewCustomer, self).get_initial()
        initial['email'] = self.request.user.email
        initial['subscription'] = Subscription.objects.filter(default=True).first()
        if 'sub' in self.request.GET and self.request.GET['sub'].isdigit():
            try:
                initial['subscription'] = Subscription.objects.get(pk=int(self.request.GET['sub']))
            except Subscription.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        form.create_new_customer(self.request.user)
        messages.add_message(
            self.request, messages.SUCCESS, _('Thank you, welcome to AppointWare'))
        return super(NewCustomer, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        # if current user is already tied to a customer that has a subscription then redirect them away
        if self.request.user.userprofile.customer and self.request.user.userprofile.customer.has_subscription():
            return redirect('dashboard')

        return super(NewCustomer, self).dispatch(*args, **kwargs)


class EditCustomer(CustomerMixin, FormView):
    template_name = 'customers/edit.html'
    form_class = CustomerForm
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super(EditCustomer, self).get_initial()
        initial['name'] = self.object.name
        initial['email'] = self.object.email
        initial['phone'] = self.object.phone
        return initial

    def form_valid(self, form):
        form.save_customer(self.object, self.request.user)
        messages.add_message(
            self.request, messages.SUCCESS, _('Successfully saved'))
        return super(EditCustomer, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.object = self.request.user.userprofile.customer

        return super(EditCustomer, self).dispatch(*args, **kwargs)
