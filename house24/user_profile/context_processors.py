from db.models.house import Message, Section, Floor, House


def add_client_info_to_template(request):
    if not request.user.is_staff:
        flats = request.user.flats.all()
        houses = House.objects.filter(flats__in=flats)
        sections = Section.objects.filter(flats__in=flats)
        floors = Floor.objects.filter(flats__in=flats)
        messages = Message.objects.filter(house__in=houses,
                                          section__in=sections,
                                          floor__in=floors,
                                          flat__in=flats,
                                          with_debt=request.user.has_debt)
        return {
            'houses': houses,
            'flats': flats,
            'messages': messages,
            'messages_count': messages.count()
        }
    else:
        return {}
