from rest_framework import generics

from rest_api import serializers

from db.models.house import Section, Floor, Flat


class SectionList(generics.ListAPIView):
    model = Section
    serializer_class = serializers.SectionSerializer

    def get_queryset(self):
        house = self.request.query_params.get('pk')
        if house:
            queryset = self.model.objects.filter(house__pk=house)
        else:
            queryset = []
        return queryset


class FloorList(generics.ListAPIView):
    model = Floor
    serializer_class = serializers.FloorSerializer

    def get_queryset(self):
        house = self.request.query_params.get('pk')
        if house:
            queryset = self.model.objects.filter(house__pk=house)
        else:
            queryset = []
        return queryset


class FlatList(generics.ListAPIView):
    model = Flat
    serializer_class = serializers.FlatSerializer

    def get_queryset(self):
        house = self.request.query_params.get('pk')
        if house:
            queryset = self.model.objects.filter(house__pk=house)
        else:
            queryset = []
        return queryset
