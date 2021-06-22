from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView
from django.http import HttpResponse
from django.db.models import Q

from user_profile.views.mixin import ListPaginatedQuery
from user_profile.forms.client_forms import SearchMessageForm

from db.models.house import Message, House, Section, Floor
from db.services.search import MessageSearch

import json


class ListClientMessagesView(ListPaginatedQuery):
    model = Message
    template_name = 'messages/list_messages_client.html'

    def get(self, request, pk):
        flats = request.user.flats.all()
        houses = House.objects.filter(flats__in=flats)
        sections = Section.objects.filter(flats__in=flats)
        floors = Floor.objects.filter(flats__in=flats)
        messages = Message.objects.exclude(excluded_receivers=request.user).filter(
            (Q(house__in=houses) | Q(section__in=sections) | Q(floor__in=floors) | Q(flat__in=flats))
        )
        message_for_all = Message.objects.exclude(excluded_receivers=request.user).filter(house__isnull=True,
                                                                                          section__isnull=True,
                                                                                          floor__isnull=True,
                                                                                          flat__isnull=True)
        instances = messages | message_for_all
        if not request.user.has_debt:
            instances = instances.exclude(with_debt=True)
        page = request.GET.get('page')
        form = SearchMessageForm(request.GET)
        if form.is_valid():
            instances = MessageSearch.search(form.cleaned_data, instances)
        return render(request, self.template_name, context={'instances': self.get_paginated_query(instances, page),
                                                            'form': form})


class ExcludeUserFromReceivingMessage(View):
    model = Message

    def get(self, request):
        pks = json.loads(request.GET.get('pk'))
        messages = Message.objects.filter(pk__in=pks)
        for message in messages:
            message.excluded_receivers.add(request.user)
            message.save()
        return HttpResponse()


class ExcludeMessage(View):
    model = Message

    def get(self, request, pk):
        message = get_object_or_404(self.model, pk=pk)
        message.excluded_receivers.add(request.user)
        message.save()
        return redirect('user_profile:list_client_messages_view', pk=request.user.pk)


class ClientMessageDetailView(DetailView):
    model = Message
    template_name = 'messages/detail_message_client.html'
    context_object_name = 'message'
