from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import InheritPermissions

from djangoldp_ep.models.__base import baseEPModel
from djangoldp_ep.models.citizen_project import CitizenProject


class Testimony(baseEPModel):
    citizen_project = models.ForeignKey(
        CitizenProject,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Projet",
        related_name="testimonies",
    )
    author_name = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Auteur"
    )
    author_picture = models.TextField(
        blank=True, null=True, verbose_name="Auteur: Photo"
    )
    content = models.TextField(blank=True, null=True, verbose_name="Contenu")

    class Meta(baseEPModel.Meta):
        # TODO: Prepare a migration for related urlids
        # container_path = "testimonies/"
        permission_classes = [InheritPermissions]
        inherit_permissions = ["citizen_project"]
        rdf_type = "energiepartagee:testimony"
        verbose_name = _("Témoignage")
        verbose_name_plural = _("Témoignages")
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "citizen_project",
            "author_name",
            "author_picture",
            "content",
        ]
