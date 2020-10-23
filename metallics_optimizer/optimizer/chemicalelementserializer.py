from rest_framework import serializers
from .models import ChemicalElement, Composition


class ChemicalElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemicalElement
        fields = "__all__"
        depth = 1


class CompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = "__all__"
