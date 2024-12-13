from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.utils import is_anonymous_user

from djangoldp_ep.models.__base import baseEPModel
from djangoldp_ep.models.actor import *
from djangoldp_ep.permissions import EPRelatedActorPermissions

ROLE_CHOICES = [("admin", "Administrateur"), ("membre", "Membre"), ("refuse", "Refusé")]


class Relatedactor(baseEPModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Acteur",
        related_name="members",
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=50,
        blank=True,
        default="",
        verbose_name="Rôle de l'utilisateur",
    )
    reminderdate = models.DateTimeField(
        blank=True, null=True, verbose_name="Date de relance"
    )

    class Meta(baseEPModel.Meta):
        permission_classes = [EPRelatedActorPermissions]
        permission_roles = {
            "member": {"perms": {"view", "add", "change", "delete"}},
            "admin": {"perms": {"view", "add", "change", "delete"}},
        }
        rdf_type = "energiepartagee:relatedactor"
        unique_together = ["user", "actor"]
        verbose_name = _("Membre")
        verbose_name_plural = _("Membres")
        depth = 1
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "user",
            "actor",
            "role",
            "reminderdate",
        ]

    def __str__(self):
        if self.actor and self.user:
            return "%s - %s" % (str(self.user), str(self.actor))
        else:
            return self.urlid

    @classmethod
    def get_mine(cls, user, role=None):
        if is_anonymous_user(user):
            return Relatedactor.objects.none()

        if role is None:
            return Relatedactor.objects.filter(user=user)

        if isinstance(role, list):
            return Relatedactor.objects.filter(user=user, role__in=role)

        return Relatedactor.objects.filter(user=user, role=role)

    @classmethod
    def get_user_actors_id(cls, user, role=None):
        return cls.get_mine(user=user, role=role).values_list("actor_id", flat=True)
