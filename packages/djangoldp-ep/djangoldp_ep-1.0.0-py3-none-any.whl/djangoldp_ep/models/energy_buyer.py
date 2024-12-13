from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import InheritPermissions

from djangoldp_ep.models.__base_named import baseEPNamedModel


class EnergyBuyer(baseEPNamedModel):

    class Meta(baseEPNamedModel.Meta):
        permission_classes = [InheritPermissions]
        inherit_permissions = ["energy_bought"]
        rdf_type = "energiepartagee:energy_buyer"
        verbose_name = _("Acheteur d'énergie")
        verbose_name_plural = _("Acheteurs d'énergies")
