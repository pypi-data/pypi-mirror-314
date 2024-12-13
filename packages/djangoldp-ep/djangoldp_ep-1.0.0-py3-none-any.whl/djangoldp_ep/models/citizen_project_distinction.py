from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import ReadOnly

from djangoldp_ep.models.__base_named import baseEPNamedModel
from djangoldp_ep.models.citizen_project import CitizenProject


class EarnedDistinction(baseEPNamedModel):
    citizen_projects = models.ManyToManyField(
        CitizenProject,
        blank=True,
        verbose_name="Projets Distingués",
        related_name="earned_distinctions",
    )

    class Meta(baseEPNamedModel.Meta):
        permission_classes = [ReadOnly]
        rdf_type = "energiepartagee:distinction"
        verbose_name = _("Distinction des projets")
        verbose_name_plural = _("Distinctions des projets")

        static_version = 1
