from django.db import models
from django.contrib import admin


class ChemicalElement(models.Model):
    """
    ORM to map chemical_element table
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    @staticmethod
    def get_or_create_unknown_element():
        """
        this method returns Unknown element if
        exist else it will create and return it
        """
        try:
            element = ChemicalElement.objects.get(name="Unknown")
        except ChemicalElement.DoesNotExist:
            element = ChemicalElement(name="Unknown")
            element.save()
        return element

    def __repr__(self):
        return self.name


class Commodity(models.Model):
    """
    ORM to map commodity table
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    inventory = models.FloatField()
    price = models.FloatField()
    chemical_element = models.ManyToManyField(
        ChemicalElement,
        through="Composition"
    )


class Composition(models.Model):
    """
    ORM to map composition table
    """
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    chemical_element = models.ForeignKey(
        ChemicalElement,
        on_delete=models.CASCADE
    )
    concentration = models.IntegerField()

    class Meta:
        unique_together = (
            "commodity",
            "chemical_element",
        )


admin.site.register(ChemicalElement)
admin.site.register(Commodity)
admin.site.register(Composition)
