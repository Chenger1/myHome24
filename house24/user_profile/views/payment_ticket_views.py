from django.shortcuts import render, get_object_or_404

from user_profile.views.mixin import ListPaginatedQuery

from db.models.house import Flat


class ListPaymentTicketsView(ListPaginatedQuery):
    model = Flat
    template_name = 'payment_tickets/list_payment_tickets_user.html'

    def get(self, request, pk):
        flat = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, context={'instances': flat.tickets.all(),
                                                            'flat': flat})
