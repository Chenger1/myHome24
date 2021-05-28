from rest_framework import serializers

from db.models.house import Section, Floor


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'house', 'name', )


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ('id', 'house', 'name', )
