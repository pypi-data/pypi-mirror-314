from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import InheritPermissions

from djangoldp_ep.models.__base_named import baseEPNamedModel


class EnergyType(baseEPNamedModel):
    installed_capacity_reference_unit = models.CharField(
        max_length=250, blank=True, null=True
    )
    yearly_proudction_ref_unit = models.CharField(max_length=250, blank=True, null=True)
    capacity_factor_ref_unit = models.CharField(max_length=250, blank=True, null=True)

    class Meta(baseEPNamedModel.Meta):
        permission_classes = [InheritPermissions]
        inherit_permissions = ["energy_production"]
        rdf_type = "energiepartagee:energy_type"
        verbose_name = _("Type d'énergie")
        verbose_name_plural = _("Types d'énergies")
        serializer_fields = baseEPNamedModel.Meta.serializer_fields + [
            "installed_capacity_reference_unit",
            "yearly_proudction_ref_unit",
            "capacity_factor_ref_unit",
        ]
