from django.utils.translation import gettext_lazy as _

from djangoldp_ep.models.__base_named import baseEPNamedModel


class Legalstructure(baseEPNamedModel):

    class Meta(baseEPNamedModel.Meta):
        rdf_type = "energiepartagee:legalstructure"
        verbose_name = _("Structure juridique")
        verbose_name_plural = _("Structures juridiques")
