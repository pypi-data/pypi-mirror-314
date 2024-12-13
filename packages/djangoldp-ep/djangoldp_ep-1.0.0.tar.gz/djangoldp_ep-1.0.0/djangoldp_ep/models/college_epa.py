from django.utils.translation import gettext_lazy as _

from djangoldp_ep.models.__base_named import baseEPNamedModel


class Collegeepa(baseEPNamedModel):

    class Meta(baseEPNamedModel.Meta):
        rdf_type = "energiepartagee:collegeepa"
        verbose_name = _("Collège EPA")
        verbose_name_plural = _("Collèges EPA")
