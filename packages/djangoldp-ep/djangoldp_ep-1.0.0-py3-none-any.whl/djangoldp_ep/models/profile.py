from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import OwnerPermissions

from djangoldp_ep.models.__base import baseEPModel


class Profile(baseEPModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Numéro de téléphone"
    )
    presentation = models.TextField(
        blank=True, null=True, verbose_name="Présentation de l'utilisateur"
    )
    picture = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        default="/img/default_avatar_user.svg",
        verbose_name="Photo de l'utilisateur",
    )
    address = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Adresse"
    )
    postcode = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="Code Postal"
    )
    city = models.CharField(max_length=250, blank=True, null=True, verbose_name="Ville")

    class Meta(baseEPModel.Meta):
        owner_field = "user"
        permission_classes = [OwnerPermissions]
        rdf_type = "energiepartagee:profile"
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "phone",
            "presentation",
            "picture",
            "address",
            "postcode",
            "city",
        ]
        verbose_name = _("Profil")
        verbose_name_plural = _("Profils")

    def __str__(self):
        if self.user:
            return str(self.user)
        else:
            return self.urlid
