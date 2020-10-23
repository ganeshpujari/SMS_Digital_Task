from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication
)
from rest_framework.permissions import IsAuthenticated

from .models import ChemicalElement, Commodity, Composition
from .chemicalelementserializer import (
    ChemicalElementSerializer, CompositionSerializer
)
from .commoditytserializer import CommoditySerializer


class ChemicalElementAPI(APIView):

    # Support both Session and Basic Authentication
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ChemicalElement.objects.all()
    serializer_class = ChemicalElementSerializer

    def get(self, request: Request, format=None):
        """
        List all chemical elements"
        """
        chemical_elements = ChemicalElement.objects.all()
        serializer = ChemicalElementSerializer(chemical_elements, many=True)
        return Response(serializer.data)


class CommodityAPI(APIView):

    # Support both Session and Basic Authentication
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Commodity.objects.all()

    def get(self, request: Request, pk: int, format=None):
        """
        Get Commodity details by id"
        """
        try:
            commodity = Commodity.objects.get(pk=pk)
        except Commodity.DoesNotExist:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        data = {
            "id": commodity.id,
            "name": commodity.name,
            "inventory": commodity.inventory,
            "price": commodity.price,
        }
        element_list = []
        for element in commodity.chemical_element.all():
            element_data = {}
            ele = {"id": element.id, "name": element.name}
            element_data["element"] = ele
            composition = Composition.objects.get(
                chemical_element_id=element.id,
                commodity_id=pk)
            element_data["percentage"] = composition.concentration
            element_list.append(element_data)
        data["chemical_composition"] = element_list
        return Response(data)

    def put(self, request: Request, pk: int, format=None):
        """
        Update Commodity details by id"
        """
        try:
            commodity = Commodity.objects.get(pk=pk)
        except Commodity.DoesNotExist:
            return Response(
                f"commodity with {pk} not found", status=status.HTTP_404_NOT_FOUND
            )
        serializer = CommoditySerializer(commodity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConcentrationAPI(APIView):

    # Support both Session and Basic Authentication
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Composition.objects.all()

    def _create_unknown_composition(
            self, total_concentration: int, commodity_id: int
    ) -> None:
        """Create unknown composition for the commodity"""
        unknown_element = ChemicalElement.get_or_create_unknown_element()
        try:
            composition = Composition.objects.get(
                commodity_id=commodity_id, chemical_element_id=unknown_element.id
            )
        except Composition.DoesNotExist:
            composition = Composition(
                commodity_id=commodity_id, chemical_element=unknown_element
            )
        composition.concentration = 100 - total_concentration
        composition.save()

    def _get_total_concentration_by_commodity(
            self, commodity: int) -> int:
        """calculate and return total concentration for commodity"""
        elements = Composition.objects.filter(commodity_id=commodity).exclude(
            chemical_element__name="Unknown"
        )
        total_percentage = 0
        for element in elements:
            total_percentage += element.concentration
        return total_percentage

    def post(self, request, format=None):
        """
        Add Composition in database"
        """
        serializer = CompositionSerializer(data=request.data)
        if serializer.is_valid():
            total_percentage = self._get_total_concentration_by_commodity(
                request.data["commodity"]
            )
            if total_percentage + request.data["concentration"] <= 100:
                serializer.save()
                self._create_unknown_composition(
                    total_percentage + request.data["concentration"],
                    request.data["commodity"],
                )
            else:
                return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Delete Composition from database"
        """
        try:
            composition = Composition.objects.get(pk=pk)
            composition.delete()
            total_percentage = self._get_total_concentration_by_commodity(
                composition.commodity.id
            )
            self._create_unknown_composition(total_percentage, composition.commodity.id)
        except Composition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
