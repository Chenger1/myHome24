from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

from django_renderpdf.views import PDFView
from django_renderpdf.helpers import render_pdf, select_template

from db.models.house import TicketTemplate, PaymentTicket
from db.models.pages import ContactsPage

from admin_panel.utils.send_mail import MailSender

import datetime
from io import BytesIO


class RenderPdfTemplate(PDFView):
    template_name = None
    prompt_download = True
    ticket = None
    template = None
    to_response = True

    def get(self, request, *args, **kwargs):
        self.ticket = get_object_or_404(PaymentTicket, pk=request.GET.get('ticket_pk'))
        if request.GET.get('html_template'):
            self.template = get_object_or_404(TicketTemplate, pk=request.GET.get('html_template'))
            self.template_name = self.template.file.name.split('/')[-1]
        else:
            self.template_name = 'pdf_ticket_template.html'
        if request.GET.get('send'):
            self.to_response = False
        return super().get(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.ticket
        context['contacts'] = ContactsPage.load()
        return context

    def render(self, request, template, context) -> HttpResponse:
        """Returns a response.

        By default, this will contain the rendered PDF, but if both ``allow_force_html``
        is ``True`` and the querystring ``html=true`` was set it will return a plain
        HTML.
        """
        if self.allow_force_html and self.request.GET.get("html", False):
            html = select_template(template).render(context)
            return HttpResponse(html)
        else:
            if self.to_response:
                response = HttpResponse(content_type="application/pdf")
                if self.prompt_download:
                    response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                        self.get_download_name()
                    )
                render_pdf(
                    template=template,
                    file_=response,
                    url_fetcher=self.url_fetcher,
                    context=context,
                )
                return response
            else:
                file = BytesIO()
                render_pdf(template=template,
                           file_=file,
                           url_fetcher=self.url_fetcher,
                           context=context)
                sender = MailSender(self.ticket.flat.owner, file, self.ticket.number)
                sender.send_email()
                return redirect('admin_panel:detail_payment_ticket_admin', pk=self.ticket.pk)

    @property
    def download_name(self):
        return f'{datetime.date.today()}_ticket_{self.ticket.number}.pdf'
