from admin_panel.views.mixins import ListInstancesMixin
from admin_panel.forms.master_forms import MasterRequestSearchForm

from db.models.house import MasterRequest


class ListMasterRequestsView(ListInstancesMixin):
    model = MasterRequest
    search_form = MasterRequestSearchForm
    template_name = 'master/list_master_requests.html'
