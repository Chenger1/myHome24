from django.db.models import Q

from db.models.house import Message, Section, Floor, House


def add_client_info_to_template(request):
    if request.user.is_authenticated and not request.user.is_staff:
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
                                                                                          flat__isnull=True,
                                                                                          owner__isnull=True)
        message_for_owner = Message.objects.filter(owner=request.user)
        instances = messages | message_for_all | message_for_owner
        if not request.user.has_debt:
            instances = instances.exclude(with_debt=True)
        return {
            'houses': houses,
            'flats': flats,
            'client_messages': instances[:10],
            'messages_count': instances.count()
        }
    else:
        return {}
