from rest_framework import serializers

from db.models.house import Section, Floor, Flat, House
from db.models.user import User


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'house', 'name', )


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ('id', 'section', 'name', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number')


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'name')


class FlatSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    house = HouseSerializer(read_only=True)

    class Meta:
        model = Flat
        fields = ('id', 'number', 'owner', 'house', )
