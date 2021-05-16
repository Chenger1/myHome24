from django.views.generic import View
from django.shortcuts import render


class SingletonView(View):
    model = None
    template_name = None
    context_object_name = 'page'

    def get(self, request):
        """
            Singleton pages have only one instance. It can be called using .load method
        :param request:
        :return: Dict['page_name': page_data]
        """

        page = self.model.load()
        return render(request, self.template_name, context={self.context_object_name: page})
