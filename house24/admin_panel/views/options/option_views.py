from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

from admin_panel.forms.system_options_forms import MeasureFormset, ServiceFormset
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.views.pages.singleton_mixin import DeleteGalleryImageMixin

from db.models.house import Measure, Service


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
            for form in formset:
                form.save()
            return redirect('admin_panel:service_measure_option')


class SaveMeasureForm(AdminPermissionMixin, View):
    def post(self, request):
        formset = MeasureFormset(request.POST, prefix='measure')
        if formset.is_valid():
            for form in formset:
                form.save()
            return redirect('admin_panel:service_measure_option')


class DeleteServiceBlock(DeleteGalleryImageMixin):
    model = Service


class DeleteMeasureBlock(DeleteGalleryImageMixin):
    model = Measure
