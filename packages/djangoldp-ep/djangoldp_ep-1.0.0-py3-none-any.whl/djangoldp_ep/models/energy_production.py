from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import InheritPermissions

from djangoldp_ep.models.__base import baseEPModel
from djangoldp_ep.models.energy_buyer import EnergyBuyer
from djangoldp_ep.models.energy_buyer_type import ContractType
from djangoldp_ep.models.energy_type import EnergyType
from djangoldp_ep.models.production_site import ProductionSite

ENERGY_PRODUCTION_TECHNOLOGIES_USED = [
    ("wood", "Bois énergie"),
    ("eolien", "Éolien"),
    ("geothermy", "Géothermie"),
    ("methan", "Méthanisation"),
    ("hydroelectricity", "Hydroélectricité"),
    ("economy", "Économies d'énergie"),
    ("floor_photo", "Photovoltaïque au sol"),
    ("ombre_photo", "Photovoltaïque en ombrière"),
    ("roof_photo", "Photovoltaïque en toiture"),
    ("floating_photo", "Photovoltaïque flottant"),
    ("heat_photo", "Solaire thermique"),
]


class EnergyProduction(baseEPModel):
    production_site = models.ForeignKey(
        ProductionSite,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Site de production",
        related_name="energy_productions",
    )
    energy_buyer = models.ForeignKey(
        EnergyBuyer,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Acheteur d'énergie",
        related_name="energy_bought",
    )
    contract_type = models.ForeignKey(
        ContractType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Type de contrat",
        related_name="contract",
    )
    energy_type = models.ForeignKey(
        EnergyType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Type d'énergie",
        related_name="energy_production",
    )
    energy_contract = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Contrat associé"
    )
    reference_unit = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Unité de référence"
    )
    estimated_capacity = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Puissance estimée"
    )
    installed_capacity = models.DecimalField(
        max_digits=50,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Puissance installée",
    )
    consumption_equivalence = models.DecimalField(
        max_digits=50,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Equivalence en nombre de foyers",
    )
    estimated_yearly_production = models.DecimalField(
        max_digits=50,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Production annuelle estimée",
    )
    technology_used = models.CharField(
        choices=ENERGY_PRODUCTION_TECHNOLOGIES_USED,
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Technologie utilisée",
    )
    estimated_injection_capacity = models.DecimalField(
        max_digits=50,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="Capacité d'injection estimée",
    )

    @property
    def estimated_yearly_producible(self):
        if self.estimated_yearly_production and self.installed_capacity:
            return self.estimated_yearly_production * 1000 / self.installed_capacity
        return 0

    class Meta(baseEPModel.Meta):
        permission_classes = [InheritPermissions]
        inherit_permissions = ["production_site"]
        rdf_type = "energiepartagee:energy_production"
        verbose_name = _("Énergie produite")
        verbose_name_plural = _("Énergies produites")
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "energy_buyer",
            "contract_type",
            "energy_type",
            "energy_contract",
            "reference_unit",
            "estimated_capacity",
            "installed_capacity",
            "consumption_equivalence",
            "estimated_yearly_production",
            "technology_used",
            "estimated_injection_capacity",
            "estimated_yearly_producible",
        ]
        depth = 1

        static_version = 1

    def __str__(self):
        if self.production_site.name:
            return self.production_site.name
        else:
            return self.urlid
