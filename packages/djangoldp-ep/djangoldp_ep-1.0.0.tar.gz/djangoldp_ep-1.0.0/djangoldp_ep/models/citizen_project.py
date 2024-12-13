from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import InheritPermissions, IPOpenPermissions

from djangoldp_ep.models.__base_named import baseEPNamedModel
from djangoldp_ep.models.actor import Actor
from djangoldp_ep.models.region import Region
from djangoldp_ep.permissions import EPRegionalAdminPermission

CITIZEN_PROJECT_STATUS_CHOICES = [
    ("draft", "Brouillon"),
    ("validation", "En cours de validation"),
    ("published", "Publié"),
    ("retired", "Dépublié"),
]


class CitizenProject(baseEPNamedModel):
    founder = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Fondateur",
        related_name="founded_projects",
    )
    short_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="description des installations de production",
    )
    city = models.CharField(max_length=250, blank=True, null=True, verbose_name="Ville")
    postcode = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Code Postal"
    )
    address = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Adresse"
    )
    # region = models.CharField(max_length=50, blank=True, null=True, verbose_name="Région")
    region = models.ForeignKey(
        Region,
        max_length=50,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Région",
        related_name="projects",
    )
    department = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Département"
    )
    action_territory = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Territoire d'action du projet",
    )
    picture = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Photo"
    )
    video = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Vidéo"
    )
    website = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Site"
    )
    facebook_link = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Facebook"
    )
    linkedin_link = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="LinkedIn"
    )
    twitter_link = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Twitter"
    )
    instagram_link = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Instragram"
    )
    contact_picture = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Contact: Photo"
    )
    contact_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Contact: Nom"
    )
    contact_first_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Contact: Prénom"
    )
    contact_email = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Contact: Email"
    )
    contact_phone = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Contact: Téléphone"
    )
    contact_visibility = models.BooleanField(
        blank=True, null=True, verbose_name="Visibilité du contact", default=False
    )
    status = models.CharField(
        choices=CITIZEN_PROJECT_STATUS_CHOICES,
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Publication",
    )
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
    production_tracking_url = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="URL monitoring du site de production",
    )
    fundraising_url = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="URL Page Collecte locale",
    )
    wp_project_url = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Lien du projet sur le site principal",
    )
    visible = models.BooleanField(
        blank=True, null=True, verbose_name="Peut être rendu visible", default=False
    )

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
            self.production_sites.filter(
                visible=True, energy_productions__technology_used__isnull=False
            )
            .values_list("energy_productions__technology_used", flat=True)
            .distinct()
        )

    @property
    def energies_produced(self):
        return set(
            self.production_sites.filter(
                visible=True, energy_productions__energy_type__name__isnull=False
            )
            .values_list("energy_productions__energy_type__name", flat=True)
            .distinct()
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
            self.production_sites.filter(
                visible=True, progress_status__isnull=False
            ).values_list("progress_status", flat=True)
        )
        for status in priority_statuses:
            if status in progresses:
                return status
        return None

    @property
    def expected_commissionning_year(self):
        return (
            self.production_sites.filter(visible=True).aggregate(
                earliest_year=models.Min("expected_commissionning_year")
            )["earliest_year"]
            or None
        )

    @property
    def effective_commissionning_year(self):
        return (
            self.production_sites.filter(
                visible=True, progress_status__iexact="exploitation"
            ).aggregate(earliest_year=models.Min("effective_commissionning_year"))[
                "earliest_year"
            ]
            or None
        )

    @property
    def installed_capacity(self):
        production_sites = self.production_sites.filter(visible=True)
        if production_sites:
            return (
                production_sites.aggregate(
                    total=models.Sum("energy_productions__installed_capacity")
                )["total"]
                or 0
            )
        return 0

    @property
    def estimated_yearly_production(self):
        production_sites = self.production_sites.filter(visible=True)
        if production_sites:
            return (
                production_sites.aggregate(
                    total=models.Sum("energy_productions__estimated_yearly_production")
                )["total"]
                or 0
            )
        return 0

    @property
    def estimated_injection_capacity(self):
        production_sites = self.production_sites.filter(visible=True)
        if production_sites:
            return (
                production_sites.aggregate(
                    total=models.Sum("energy_productions__estimated_injection_capacity")
                )["total"]
                or 0
            )
        return 0

    @property
    def consumption_equivalence(self):
        production_sites = self.production_sites.filter(visible=True)
        if production_sites:
            return (
                production_sites.aggregate(
                    total=models.Sum("energy_productions__consumption_equivalence")
                )["total"]
                or 0
            )
        return 0

    @property
    def total_investment_budget(self):
        production_sites = self.production_sites.filter(visible=True)
        if production_sites:
            return (
                production_sites.aggregate(total=models.Sum("total_investment_budget"))[
                    "total"
                ]
                or 0
            )
        return 0

    class Meta(baseEPNamedModel.Meta):
        permission_classes = [
            IPOpenPermissions | InheritPermissions | EPRegionalAdminPermission
        ]
        inherit_permissions = ["founder"]
        rdf_type = "energiepartagee:citizen_project"
        nested_fields = [
            "communication_profile",
            "earned_distinctions",
            "testimonies",
            "production_sites",
        ]
        serializer_fields = baseEPNamedModel.Meta.serializer_fields + [
            "visible",
            "technologies_used",
            "technology_used",
            "energies_produced",
            "energy_type",
            "progress_status",
            "expected_commissionning_year",
            "effective_commissionning_year",
            "installed_capacity",
            "estimated_yearly_production",
            "estimated_injection_capacity",
            "consumption_equivalence",
            "total_investment_budget",
            "short_description",
            "city",
            "postcode",
            "address",
            "department",
            "action_territory",
            "picture",
            "video",
            "website",
            "facebook_link",
            "linkedin_link",
            "twitter_link",
            "instagram_link",
            "contact_picture",
            "contact_name",
            "contact_first_name",
            "contact_email",
            "contact_phone",
            "contact_visibility",
            "status",
            "lat",
            "lng",
            "production_tracking_url",
            "fundraising_url",
            "wp_project_url",
            "founder",
            "region",
            "communication_profile",
            "earned_distinctions",
            "testimonies",
            "production_sites",
        ]
        verbose_name = _("Projet Citoyen")
        verbose_name_plural = _("Projets Citoyens")

        static_version = 1
        static_params = {
            "search-fields": "visible",
            "search-terms": True,
            "search-method": "exact",
        }
