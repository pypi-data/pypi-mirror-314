from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import (AnonymousReadOnly, IPOpenPermissions,
                                   ReadAndCreate)

from djangoldp_ep.models.__base import baseEPModel
from djangoldp_ep.models.college import *
from djangoldp_ep.models.college_epa import *
from djangoldp_ep.models.discount import *
from djangoldp_ep.models.integration_step import *
from djangoldp_ep.models.intervention_zone import *
from djangoldp_ep.models.legal_structure import *
from djangoldp_ep.models.region import *
from djangoldp_ep.models.regional_network import *
from djangoldp_ep.permissions import (EPActorPermission,
                                      EPRegionalAdminPermission)

ACTORTYPE_CHOICES = [
    ("soc_citoy", "Sociétés Citoyennes"),
    ("collectivite", "Collectivités"),
    ("structure", "Structures d’Accompagnement"),
    ("partenaire", "Partenaires"),
]

CATEGORY_CHOICES = [
    ("collectivite", "Collectivités"),
    ("porteur_dev", "Porteurs de projet en développement"),
    ("porteur_exploit", "Porteurs de projet en exploitation"),
    ("partenaire", "Partenaires"),
]


class Actor(baseEPModel):
    shortname = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Nom court de l'acteur"
    )
    longname = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Nom long de l'acteur"
    )
    address = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Adresse"
    )
    complementaddress = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Complément d'adresse"
    )
    postcode = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Code Postal"
    )
    city = models.CharField(max_length=250, blank=True, null=True, verbose_name="Ville")
    region = models.ForeignKey(
        Region,
        max_length=50,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Région",
        related_name="actors",
    )
    website = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Site internet"
    )
    mail = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Adresse mail"
    )
    phone = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Numéro de téléphone"
    )
    iban = models.CharField(max_length=35, blank=True, null=True, verbose_name="IBAN")
    lat = models.DecimalField(
        max_digits=30,
        decimal_places=25,
        blank=True,
        null=True,
        verbose_name="Latitude",
    )
    lng = models.DecimalField(
        max_digits=30,
        decimal_places=25,
        blank=True,
        null=True,
        verbose_name="Longitude",
    )
    status = models.BooleanField(
        verbose_name="Adhérent", blank=True, null=True, default=False
    )
    regionalnetwork = models.ForeignKey(
        Regionalnetwork,
        blank=True,
        null=True,
        max_length=250,
        on_delete=models.SET_NULL,
        verbose_name="Paiement à effectuer à",
    )
    actortype = models.CharField(
        choices=ACTORTYPE_CHOICES,
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Type d'acteur",
    )
    category = models.CharField(
        choices=CATEGORY_CHOICES,
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Catégorie de cotisant",
    )
    numberpeople = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre d'habitants"
    )
    numberemployees = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre d'employés"
    )
    turnover = models.IntegerField(
        blank=True, null=True, verbose_name="Chiffre d'affaires"
    )
    presentation = models.TextField(
        blank=True, null=True, verbose_name="Présentation/objet de la structure"
    )
    interventionzone = models.ManyToManyField(
        Interventionzone,
        blank=True,
        max_length=50,
        verbose_name="Zone d'intervention",
        related_name="actors",
    )
    logo = models.CharField(
        blank=True,
        max_length=250,
        null=True,
        default="https://moncompte.energie-partagee.org/img/default_avatar_actor.svg",
        verbose_name="Logo",
    )
    legalstructure = models.ForeignKey(
        Legalstructure,
        max_length=50,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Structure Juridique",
        related_name="actors",
    )
    legalrepresentant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_requests_created",
        blank=True,
        null=True,
        verbose_name="Représentant légal",
    )
    managementcontact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Contact Gestion",
    )
    adhmail = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Mail pour compte espace ADH"
    )
    siren = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="SIREN ou RNA"
    )
    collegeepa = models.ForeignKey(
        Collegeepa,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Collège EPA",
        related_name="actors",
    )
    college = models.ForeignKey(
        College,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Collège",
        related_name="actors",
    )
    actorcomment = models.TextField(
        blank=True, null=True, verbose_name="Commentaires de l'acteur"
    )
    signataire = models.BooleanField(
        blank=True, null=True, verbose_name="Signataire de la charte EP", default=False
    )
    renewed = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Adhérent sur l'année en cours",
        default=True,
    )
    integrationstep = models.OneToOneField(
        Integrationstep,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Espace administrateur",
        related_name="actor",
    )
    visible = models.BooleanField(
        blank=True, null=True, verbose_name="Peut être rendu visible", default=False
    )
    villageoise = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="réseau des Centrales Villageoises",
        default=False,
    )

    @property
    def name(self):
        if self.shortname and self.longname:
            return "%s - %s" % (self.shortname, self.longname)
        elif self.shortname:
            return "%s" % (self.shortname)
        elif self.longname:
            return "%s" % (self.longname)
        else:
            return self.urlid

    @property
    def technology_used(self):
        technologies_used = self.technologies_used
        if technologies_used and len(technologies_used) > 1:
            if len(list(filter(lambda s: "photo" not in s, technologies_used))) > 1:
                return "multi"
            return "multi_sol"
        else:
            return technologies_used.pop() if technologies_used else "unknown"

    @property
    def energy_type(self):
        energy_produced = self.energies_produced
        if energy_produced and len(energy_produced) > 1:
            return "multi"
        return energy_produced.pop() if energy_produced else "unknown"

    @property
    def technologies_used(self):
        return set(
            self.founded_projects.filter(
                visible=True,
                production_sites__energy_productions__technology_used__isnull=False,
            )
            .values_list(
                "production_sites__energy_productions__technology_used", flat=True
            )
            .distinct()
        )

    @property
    def energies_produced(self):
        return set(
            self.founded_projects.filter(
                visible=True,
                production_sites__energy_productions__energy_type__name__isnull=False,
            )
            .values_list(
                "production_sites__energy_productions__energy_type__name", flat=True
            )
            .distinct()
        )

    @property
    def is_epi(self):
        return (
            self.capital_distribution.shareholders.filter(
                actor__longname="Énergie Partagée Investissement"
            ).count()
            > 0
        )

    @property
    def progress_status(self):
        priority_statuses = [
            "exploitation",
            "construction",
            "development",
            "emergence",
            "appeal",
            "aborted",
        ]
        progresses = set(
            self.founded_projects.filter(
                visible=True, production_sites__progress_status__isnull=False
            ).values_list("production_sites__progress_status", flat=True)
        )
        for status in priority_statuses:
            if status in progresses:
                return status
        return None

    def get_next_contribution_amount(self):
        """:return: the amount an actor should contribute in their next contribution"""
        amount = 0

        # Collectivity: 2c€ * Habitants - +50€ -1000€
        if self.category == CATEGORY_CHOICES[0][0]:
            if self.numberpeople:
                amount = 0.02 * self.numberpeople
                if amount < 50 or amount == 0:
                    amount = 50
                elif amount > 1000:
                    amount = 1000
            else:
                amount = 50
        # Porteur_dev: 50€
        elif self.category == CATEGORY_CHOICES[1][0]:
            amount = 50
        # Porteur_exploit: 0.5% CA +50€ -1000€
        elif self.category == CATEGORY_CHOICES[2][0]:
            if self.turnover:
                amount = 0.005 * self.turnover
                if amount < 50:
                    amount = 50
                elif amount > 1000:
                    amount = 1000
            else:
                amount = 50
        # Partenaire:
        #   - 1 to 4 salariés: 100€
        #   - 5 to 10 salariés: 250€
        #   - > 10 salariés: 400€
        elif self.category == CATEGORY_CHOICES[3][0]:
            if self.numberemployees:
                if self.numberemployees < 5:
                    amount = 100
                elif self.numberemployees <= 10:
                    amount = 250
                elif self.numberemployees > 10:
                    amount = 400
            else:
                amount = 100
        # apply villageoise discount for the actors
        if self.villageoise is True:
            villageoise = Discount.objects.get(name="villageoise")
            discountvillageoise = villageoise.amount
            amount = amount * (100 - float(discountvillageoise)) / 100
        return amount

    class Meta(baseEPModel.Meta):
        ordering = ["shortname"]
        permission_classes = [
            AnonymousReadOnly
            & (
                IPOpenPermissions
                | EPActorPermission
                | EPRegionalAdminPermission
                | ReadAndCreate
            )
        ]
        permission_roles = {
            "member": {"perms": {"view", "add"}},
            "admin": {"perms": {"view", "add", "change", "delete"}},
        }
        nested_fields = [
            "members",
            "integrationstep",
            "contributions",
            "capital_distribution",
            "founded_projects",
            "shareholders",
            "partner_links",
        ]
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "shortname",
            "longname",
            "visible",
            "technology_used",
            "energy_type",
            "progress_status",
            "is_epi",
            "address",
            "complementaddress",
            "postcode",
            "city",
            "website",
            "mail",
            "phone",
            "iban",
            "lat",
            "lng",
            "status",
            "actortype",
            "category",
            "numberpeople",
            "numberemployees",
            "turnover",
            "presentation",
            "logo",
            "adhmail",
            "siren",
            "actorcomment",
            "signataire",
            "renewed",
            "villageoise",
            "region",
            "regionalnetwork",
            "legalstructure",
            "legalrepresentant",
            "managementcontact",
            "collegeepa",
            "college",
            "integrationstep",
            "interventionzone",
            "members",
            "contributions",
            "capital_distribution",
            "founded_projects",
            "shareholders",
            "partner_links",
        ]

        rdf_type = "energiepartagee:actor"
        verbose_name = _("Acteur")
        verbose_name_plural = _("Acteurs")

        static_version = 1
        static_params = {
            "search-fields": "visible",
            "search-terms": True,
            "search-method": "exact",
        }

    def __str__(self):
        return self.name
