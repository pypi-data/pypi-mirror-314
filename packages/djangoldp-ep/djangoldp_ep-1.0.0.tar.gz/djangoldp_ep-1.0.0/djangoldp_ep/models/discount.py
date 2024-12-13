from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_ep.models.__base_named import baseEPNamedModel


class Discount(baseEPNamedModel):
    amount = models.DecimalField(
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name="Montant de la réduction (%)",
    )

    class Meta(baseEPNamedModel.Meta):
        rdf_type = "energiepartagee:discount"
        serializer_fields = baseEPNamedModel.Meta.serializer_fields + ["amount"]
        verbose_name = _("Réduction")
        verbose_name_plural = _("Réductions")
