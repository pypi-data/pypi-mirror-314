from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import ReadOnly

from djangoldp_ep.models.__base_named import baseEPNamedModel
from djangoldp_ep.models.production_site import ProductionSite


class SiteEarnedDistinction(baseEPNamedModel):
    production_sites = models.ManyToManyField(
        ProductionSite,
        blank=True,
        verbose_name="Sites de Production Distingués",
        related_name="earned_distinctions",
    )

    class Meta(baseEPNamedModel.Meta):
        permission_classes = [ReadOnly]
        rdf_type = "energiepartagee:distinction"
        verbose_name = _("Distinction des sites")
        verbose_name_plural = _("Distinctions des sites")
        static_version = 1
