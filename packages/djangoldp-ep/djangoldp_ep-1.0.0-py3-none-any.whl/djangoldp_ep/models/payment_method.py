from django.utils.translation import gettext_lazy as _

from djangoldp_ep.models.__base_named import baseEPNamedModel


class Paymentmethod(baseEPNamedModel):

    class Meta(baseEPNamedModel.Meta):
        rdf_type = "energiepartagee:paymentmethod"
        verbose_name = _("Méthode de paiement")
        verbose_name_plural = _("Méthodes de paiements")
