from rest_framework import serializers
from .models import Commodity, Composition, ChemicalElement
from .chemicalelementserializer import ChemicalElementSerializer


class CompositionSerializer(serializers.ModelSerializer):
    chemical_element = ChemicalElementSerializer(many=True)

    class Meta:
        model = Composition
        fields = ("chemical_element",)


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ("id", "name", "price")
        depth = 1
