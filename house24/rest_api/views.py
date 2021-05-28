from rest_framework import generics

from rest_api.serializers import SectionSerializer, FloorSerializer

from db.models.house import Section, Floor


class SectionList(generics.ListAPIView):
    model = Section
    serializer_class = SectionSerializer

    def get_queryset(self):
        house = self.request.query_params.get('pk')
        if house:
            queryset = self.model.objects.filter(house__pk=house)
        else:
            queryset = []
        return queryset


class FloorList(generics.ListAPIView):
    model = Floor
    serializer_class = FloorSerializer

    def get_queryset(self):
        house = self.request.query_params.get('pk')
        if house:
            queryset = self.model.objects.filter(house__pk=house)
        else:
            queryset = []
        return queryset
