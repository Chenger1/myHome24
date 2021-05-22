from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404


class DeleteInstanceView(View):
    model = None
    redirect_url = None

    def get(self, request, pk):
        inst = get_object_or_404(self.model, pk=pk)
        inst.delete()
        return redirect(self.redirect_url)
