from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.master_forms import MasterRequestSearchForm, CreateMasterRequestForm

from db.models.house import MasterRequest, Flat
from db.models.user import User


class ListMasterRequestsView(ListInstancesMixin):
    model = MasterRequest
    search_form = MasterRequestSearchForm
    template_name = 'master/list_master_requests.html'


class CreateMasterRequestView(AdminPermissionMixin, CreateView):
    model = MasterRequest
    form_class = CreateMasterRequestForm
    template_name = 'master/create_master_request_admin.html'
    success_url = reverse_lazy('admin_panel:list_master_requests_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flats'] = Flat.objects.all()
        context['masters'] = User.objects.filter(is_staff=True)
        return context


class UpdateMasterRequestView(AdminPermissionMixin, UpdateView):
    model = MasterRequest
    form_class = CreateMasterRequestForm
    template_name = 'master/create_master_request_admin.html'
    success_url = reverse_lazy('admin_panel:list_master_requests_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flats'] = Flat.objects.all()
        context['masters'] = User.objects.filter(is_staff=True)
        return context


class DeleteMasterRequest(DeleteInstanceView):
    model = MasterRequest
    redirect_url = 'admin_panel:list_master_requests_admin'


class DetailMasterRequest(AdminPermissionMixin, DetailView):
    model = MasterRequest
    template_name = 'master/detail_master_request_admin.html'
    context_object_name = 'req'
