from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import InheritPermissions

from djangoldp_ep.models.__base import baseEPModel
from djangoldp_ep.models.citizen_project import CitizenProject

COMMUNICATION_PROFILE_REPLICABILITY_CHOICES = [
    ("easy", "Facilement"),
    ("hard", "Difficilement"),
    ("no", "Non"),
    ("unknown", "Je ne sais pas"),
]


class CommunicationProfile(baseEPModel):
    citizen_project = models.OneToOneField(
        CitizenProject,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Projet",
        related_name="communication_profile",
    )
    is_featured = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="Mis en avant?"
    )
    crowdfunding_url = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="URL Crowdfunding"
    )
    long_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description générale du projet",
    )
    star_initiative_briefing = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Briefing projet star"
    )
    stakes_description = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Enjeux"
    )
    replicability = models.CharField(
        choices=COMMUNICATION_PROFILE_REPLICABILITY_CHOICES,
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Réplicabilité",
    )
    additional_informations = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Infos diverses"
    )

    class Meta(baseEPModel.Meta):
        permission_classes = [InheritPermissions]
        inherit_permissions = ["citizen_project"]
        rdf_type = "energiepartagee:communication_profile"
        verbose_name = _("Profil de communication")
        verbose_name_plural = _("Profils de communication")
        static_version = 1
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "citizen_project",
            "is_featured",
            "crowdfunding_url",
            "long_description",
            "star_initiative_briefing",
            "stakes_description",
            "replicability",
            "additional_informations",
        ]
