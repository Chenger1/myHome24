from db.models.house import House


class HouseSearch:
    @staticmethod
    def search(form_data):
        return House.objects.filter(name__icontains=form_data['name'], address__icontains=form_data['address'])
