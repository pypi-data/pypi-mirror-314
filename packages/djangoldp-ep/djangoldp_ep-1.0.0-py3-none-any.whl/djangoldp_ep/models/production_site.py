from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import InheritPermissions

from djangoldp_ep.models.__base_named import baseEPNamedModel
from djangoldp_ep.models.citizen_project import CitizenProject
from djangoldp_ep.models.region import Region
from djangoldp_ep.permissions import EPRegionalAdminPermission

PROGRESS_STATUS_CHOICES = [
    ("emergence", "Émergence"),
    ("development", "Développement"),
    ("construction", "Construction"),
    ("exploitation", "Exploitation"),
    ("appeal", "Fin d'exploitation"),
    ("aborted", "Projet abandonné"),
]


class ProductionSite(baseEPNamedModel):
    citizen_project = models.ForeignKey(
        CitizenProject,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Projet citoyen",
        related_name="production_sites",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    progress_status = models.CharField(
        choices=PROGRESS_STATUS_CHOICES,
        max_length=25,
        blank=True,
        null=True,
        verbose_name="Avancement",
    )
    total_development_budget = models.DecimalField(
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Budget total de développement",
    )
    total_investment_budget = models.DecimalField(
        max_digits=50,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Budget total d'investissement",
    )
    yearly_turnover = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Chiffre d'affaire annuel"
    )
    address = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Adresse"
    )
    postcode = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Code Postal"
    )
    city = models.CharField(max_length=250, blank=True, null=True, verbose_name="Ville")
    department = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Département"
    )
    region = models.ForeignKey(
        Region,
        max_length=50,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Région",
        related_name="production_sites",
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
    expected_commissionning_year = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="Année de mise en service prévue",
    )
    effective_commissionning_year = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="Année de mise en service effective",
    )
    picture = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Photo"
    )
    investment_capacity_ratio = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Ratio investissement par puissance €/kW",
    )
    grants_earned_amount = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Montant des subventions reçues pour le Site de production (en €)",
    )
    production_tracking_url = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="URL monitoring du site de production",
    )
    visible = models.BooleanField(
        blank=True, null=True, verbose_name="Peut être rendu visible", default=False
    )
    old_visible = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="Sera rendu visible si projet parent le devient",
        default=False,
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
        energy_productions = self.energy_productions.filter(
            technology_used__isnull=False
        )
        if energy_productions:
            return (
                set(
                    energy_productions.values_list(
                        "technology_used", flat=True
                    ).distinct()
                )
                if self.visible
                else None
            )
        return None

    @property
    def energies_produced(self):
        energy_productions = self.energy_productions.filter(
            energy_type__name__isnull=False
        )
        if energy_productions:
            return (
                set(
                    energy_productions.values_list(
                        "energy_type__name", flat=True
                    ).distinct()
                )
                if self.visible
                else None
            )
        return None

    class Meta(baseEPNamedModel.Meta):
        permission_classes = [InheritPermissions | EPRegionalAdminPermission]
        inherit_permissions = ["citizen_project"]
        rdf_type = "energiepartagee:production_site"
        nested_fields = [
            "citizen_project",
            "partner_links",
            "energy_productions",
            "earned_distinctions",
        ]
        serializer_fields = baseEPNamedModel.Meta.serializer_fields + [
            "visible",
            "technology_used",
            "energy_type",
            "description",
            "progress_status",
            "energies_produced",
            "total_development_budget",
            "total_investment_budget",
            "yearly_turnover",
            "address",
            "postcode",
            "city",
            "department",
            "region",
            "lat",
            "lng",
            "expected_commissionning_year",
            "effective_commissionning_year",
            "picture",
            "investment_capacity_ratio",
            "grants_earned_amount",
            "production_tracking_url",
            "partner_links",
            "energy_productions",
            "earned_distinctions",
            "citizen_project",
        ]
        verbose_name = _("Site de production")
        verbose_name_plural = _("Sites de productions")

        static_version = 1
        static_params = {
            "search-fields": "visible",
            "search-terms": True,
            "search-method": "exact",
        }
