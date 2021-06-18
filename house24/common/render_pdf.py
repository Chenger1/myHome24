from django.shortcuts import get_object_or_404

from django_renderpdf.views import PDFView

from db.models.house import TicketTemplate, PaymentTicket

import datetime


class RenderPdfTemplate(PDFView):
    template_name = None
    prompt_download = True
    ticket = None
    template = None

    def get(self, request, *args, **kwargs):
        self.ticket = get_object_or_404(PaymentTicket, pk=request.GET.get('ticket_pk'))
        self.template = get_object_or_404(TicketTemplate, pk=request.GET.get('html_template'))
        self.template_name = self.template.file.name.split('/')[-1]
        return super().get(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_number'] = self.ticket.number
        context['ticket_sum'] = self.ticket.sum
        return context

    @property
    def download_name(self):
        return f'{datetime.date.today()}_ticket_{self.ticket.number}.pdf'
