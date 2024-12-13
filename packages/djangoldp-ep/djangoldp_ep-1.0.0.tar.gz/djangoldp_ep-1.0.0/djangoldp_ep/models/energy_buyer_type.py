from django.utils.translation import gettext_lazy as _

from djangoldp_ep.models.__base_named import baseEPNamedModel


class ContractType(baseEPNamedModel):

    class Meta(baseEPNamedModel.Meta):
        rdf_type = "energiepartagee:contract_type"
        verbose_name = _("Type de contrat")
        verbose_name_plural = _("Types de contrats")
