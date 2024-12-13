from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import ReadOnly

from djangoldp_ep.models.__base_named import baseEPNamedModel
from djangoldp_ep.permissions import EPRegionalAdminPermission


class Region(baseEPNamedModel):
    isocode = models.CharField(
        max_length=6, blank=True, null=True, verbose_name="code ISO"
    )
    acronym = models.CharField(
        max_length=6, blank=True, null=True, verbose_name="Acronyme"
    )
    admins = models.ManyToManyField(
        get_user_model(),
        related_name="admin_regions",
        blank=True,
        verbose_name="Super Admins",
    )

    class Meta(baseEPNamedModel.Meta):
        permission_classes = [ReadOnly | EPRegionalAdminPermission]
        rdf_type = "energiepartagee:region"
        serializer_fields = baseEPNamedModel.Meta.serializer_fields + [
            "isocode",
            "acronym",
        ]
        verbose_name = _("Région")
        verbose_name_plural = _("Régions")
        static_version = 1
