from django.utils.translation import gettext_lazy as _

from djangoldp_ep.models.__base_named import baseEPNamedModel


class Interventionzone(baseEPNamedModel):

    class Meta(baseEPNamedModel.Meta):
        rdf_type = "energiepartagee:interventionzone"
        verbose_name = _("Zone d'intervention")
        verbose_name_plural = _("Zones d'interventions")
