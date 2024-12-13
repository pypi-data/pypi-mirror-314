from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import InheritPermissions

from djangoldp_ep.models.__base import baseEPModel
from djangoldp_ep.models.__base_named import baseEPNamedModel
from djangoldp_ep.models.actor import Actor
from djangoldp_ep.models.production_site import ProductionSite


class PartnerLinkType(baseEPNamedModel):

    class Meta(baseEPNamedModel.Meta):
        rdf_type = "energiepartagee:partner_link_type"
        verbose_name = _("Type de lien de partenariat")
        verbose_name_plural = _("Types de liens de partenariat")


class PartnerLink(baseEPModel):
    link_type = models.ForeignKey(
        PartnerLinkType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Type de lien de partenariat",
        related_name="partner_links",
    )
    production_site = models.ForeignKey(
        ProductionSite,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Site de production",
        related_name="partner_links",
    )
    actor = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Acteurs",
        related_name="partner_links",
    )

    class Meta(baseEPModel.Meta):
        ordering = ["production_site__name"]
        permission_classes = [InheritPermissions]
        inherit_permissions = ["production_site"]
        rdf_type = "energiepartagee:partner_link"
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "link_type",
            "production_site",
            "actor",
        ]
        verbose_name = _("Lien de partenariat")
        verbose_name_plural = _("Liens de partenariat")

    def __str__(self):
        if self.actor and self.production_site and self.link_type:
            if (
                self.actor.longname
                and self.production_site.name
                and self.link_type.name
            ):
                return "Actor {} - Production Site {} - Type {}".format(
                    self.actor.longname, self.production_site.name, self.link_type.name
                )
        return self.urlid
