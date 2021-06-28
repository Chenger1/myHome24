from django.views.generic import View, UpdateView, ListView, CreateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from admin_panel.forms.system_options_forms import MeasureFormset, ServiceFormset, CredentialsForm, PaymentItemForm
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.views.mixins import DeleteInstanceView

from db.models.house import PaymentItem
from db.models.pages import Credentials


class ServiceOptionView(AdminPermissionMixin, View):
    template_name = 'options/service_measure.html'
    formsets = {
        'services': ServiceFormset,
        'measure': MeasureFormset
    }

    def get(self, request):
        service_formset = ServiceFormset(prefix='services')
        measure_formset = MeasureFormset(prefix='measure')

        return render(request, self.template_name, context={'service_formset': service_formset,
                                                            'measure_formset': measure_formset})

    def post(self, request, prefix):
        formset = self.formsets[prefix](request.POST, prefix=prefix)
        if formset.is_valid():
            for form in formset:
                form.save()
                return redirect('admin_panel:')
        else:
            service_formset = ServiceFormset(prefix='services')
            measure_formset = MeasureFormset(prefix='measure')
            return render(request, self.template_name, context={'service_formset': service_formset,
                                                                'measure_formset': measure_formset,
                                                                'errors': formset.errors})


class SaveServiceForm(AdminPermissionMixin, View):
    def post(self, request):
        formset = ServiceFormset(request.POST, prefix='services')
        if formset.is_valid():
            formset.save()
        return redirect('admin_panel:service_measure_option')


class SaveMeasureForm(AdminPermissionMixin, View):
    def post(self, request):
        formset = MeasureFormset(request.POST, prefix='measure')
        if formset.is_valid():
            formset.save()
        return redirect('admin_panel:service_measure_option')


class CredentialsView(AdminPermissionMixin, UpdateView):
    model = Credentials
    form_class = CredentialsForm
    context_object_name = 'form'
    template_name = 'options/credentials.html'

    def get_object(self, queryset=None):
        return self.model.load()


class PaymentItemsListView(ListView):
    model = PaymentItem
    context_object_name = 'items'
    template_name = 'options/payment_items/payment_items_list.html'
    paginate_by = 20


class PaymentItemsListViewByTypeAscending(PaymentItemsListView):
    def get_queryset(self):
        return super().get_queryset().order_by('-type')


class PaymentItemsListViewByTypeDescending(PaymentItemsListView):
    def get_queryset(self):
        return super().get_queryset().order_by('type')


class CreatePaymentItemView(CreateView):
    model = PaymentItem
    form_class = PaymentItemForm
    context_object_name = 'form'
    template_name = 'options/payment_items/create_payment_item.html'
    success_url = reverse_lazy('admin_panel:payment_items_admin')


class UpdatePaymentItemView(UpdateView):
    model = PaymentItem
    form_class = PaymentItemForm
    context_object_name = 'form'
    template_name = 'options/payment_items/create_payment_item.html'
    success_url = reverse_lazy('admin_panel:payment_items_admin')


class DeletePaymentItemView(DeleteInstanceView):
    model = PaymentItem
    redirect_url = 'admin_panel:payment_items_admin'
