from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from admin_panel.views.mixins import ListInstancesMixin, DeleteInstanceView
from admin_panel.permission_mixin import AdminPermissionMixin
from admin_panel.forms.master_forms import MasterRequestSearchForm, CreateMasterRequestForm

from db.models.house import MasterRequest, Flat
from db.models.user import User
from db.services.search import MasterRequestSearch


class ListMasterRequestsView(ListInstancesMixin):
    model = MasterRequest
    search_form = MasterRequestSearchForm
    template_name = 'master/list_master_requests.html'
    search_obj = MasterRequestSearch


class ListMasterRequestsNumberAscendingView(ListMasterRequestsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-pk')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('-pk')
        return queryset


class ListMasterRequestsNumberDescendingView(ListMasterRequestsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('pk')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('pk')
        return queryset


class ListMasterRequestsDateAscendingView(ListMasterRequestsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('-date')
        return queryset


class ListMasterRequestsDateDescendingView(ListMasterRequestsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('date')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('date')
        return queryset


class ListMasterRequestsTypeAscendingView(ListMasterRequestsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-type')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('-type')
        return queryset


class ListMasterRequestsTypeDescendingView(ListMasterRequestsView):
    def get_queryset(self):
        queryset = super().get_queryset().order_by('type')
        return queryset

    def get_filtered_query(self, form_data):
        queryset = super().get_filtered_query(form_data).order_by('type')
        return queryset


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
