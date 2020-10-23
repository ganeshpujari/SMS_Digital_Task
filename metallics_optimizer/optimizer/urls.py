from django.urls import path
from .views import ChemicalElementAPI, CommodityAPI, ConcentrationAPI

urlpatterns = [
    path('chemical_elements/', ChemicalElementAPI.as_view()),
    path('concentration/', ConcentrationAPI.as_view()),
    path('concentration/<int:pk>/', ConcentrationAPI.as_view()),
    path('commodity/<int:pk>/', CommodityAPI.as_view()),
]
