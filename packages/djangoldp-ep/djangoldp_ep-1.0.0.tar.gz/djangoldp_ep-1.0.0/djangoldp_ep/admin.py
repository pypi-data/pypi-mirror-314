from django.conf import settings
from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin

from djangoldp_ep.models import *


@admin.register(
    CommunicationProfile,
    SAPermission,
    Testimony,
)
class EmptyAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class EPModelAdmin(DjangoLDPAdmin):
    list_display = ("urlid", "creation_date", "update_date")
    readonly_fields = ("urlid", "creation_date", "update_date")
    exclude = ("is_backlink", "allow_create_backlink")
    search_fields = ["urlid"]
    extra = 0


@admin.register(
    College,
    Collegeepa,
    Discount,
    Interventionzone,
    Legalstructure,
    Paymentmethod,
    EnergyBuyer,
    EnergyType,
    ContractType,
    PartnerLinkType,
)
class EPNamedModelAdmin(EPModelAdmin):
    list_display = ("urlid", "name", "creation_date", "update_date")
    search_fields = ["urlid", "name"]


@admin.register(Integrationstep)
class EPIntegrationstepAdmin(EPModelAdmin):
    list_display = (
        "urlid",
        "actor",
    )
    search_fields = [
        "actor__longname",
        "actor__shortname",
    ]
    list_filter = (
        "packagestep",
        "adhspacestep",
        "adhliststep",
        "regionalliststep",
    )
    ordering = ["actor"]


@admin.register(Regionalnetwork)
class EPRegionalnetworkAdmin(EPNamedModelAdmin):
    filter_horizontal = ("colleges",)


@admin.register(PartnerLink)
class EPPartnerLinkAdmin(EPModelAdmin):
    list_display = (
        "urlid",
        "actor",
        "link_type",
        "production_site",
        "creation_date",
        "update_date",
    )
    search_fields = [
        "link_type__name",
        "production_site__name",
        "actor__longname",
        "actor__shortname",
    ]
    list_filter = ("link_type",)
    ordering = ["actor"]


@admin.register(EnergyProduction)
class EPEnergyProductionAdmin(EPModelAdmin):
    list_display = (
        "urlid",
        "production_site",
        "energy_type",
        "energy_buyer",
        "creation_date",
        "update_date",
    )
    search_fields = [
        "production_site__name",
        "energy_type__name",
        "energy_buyer__name",
    ]
    list_filter = (
        "energy_type",
        "energy_buyer",
    )
    ordering = ["production_site", "energy_type", "energy_buyer"]


@admin.register(Profile)
class EPProfileAdmin(EPModelAdmin):
    list_display = ("urlid", "user", "creation_date", "update_date")
    search_fields = ["user__first_name", "user__last_name", "urlid", "user__urlid"]
    ordering = ["user"]


@admin.register(Region)
class EPRegionAdmin(EPNamedModelAdmin):
    filter_horizontal = ("admins",)


@admin.register(EarnedDistinction)
class EPDistinctionAdmin(EPNamedModelAdmin):
    filter_horizontal = ("citizen_projects",)


@admin.register(SiteEarnedDistinction)
class EPSiteEarnedDistinctionAdmin(EPNamedModelAdmin):
    filter_horizontal = ("production_sites",)


class TestimonyInline(admin.TabularInline):
    model = Testimony
    fk_name = "citizen_project"
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


class CommunicationProfileInline(admin.StackedInline):
    model = CommunicationProfile
    fk_name = "citizen_project"
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(CitizenProject)
class CitizenProjectAdmin(EPNamedModelAdmin):
    list_display = ("urlid", "founder", "name", "creation_date", "update_date")
    list_filter = (
        "status",
        "region",
        "visible",
        ("lat", admin.EmptyFieldListFilter),
        ("lng", admin.EmptyFieldListFilter),
    )
    search_fields = ["urlid", "name", "founder__longname", "founder__shortname"]
    ordering = ["founder__longname", "name"]
    inlines = [CommunicationProfileInline, TestimonyInline]


@admin.register(CapitalDistribution)
class CapitalDistributionAdmin(EPModelAdmin):
    list_display = ("urlid", "actor", "creation_date", "update_date")
    search_fields = ["actor__longname", "actor__shortname"]
    ordering = ["actor"]


@admin.register(Shareholder)
class ShareholderAdmin(EPModelAdmin):
    list_display = (
        "urlid",
        "capital_distribution",
        "actor",
        "creation_date",
        "update_date",
    )
    search_fields = [
        "capital_distribution__actor__longname",
        "capital_distribution__actor__shortname",
        "actor__longname",
        "actor__shortname",
    ]
    ordering = ["capital_distribution"]


@admin.register(ProductionSite)
class ProductionSiteAdmin(EPNamedModelAdmin):
    list_display = ("urlid", "name", "project", "actor", "creation_date", "update_date")
    list_filter = (
        "progress_status",
        "region",
        "visible",
        ("lat", admin.EmptyFieldListFilter),
        ("lng", admin.EmptyFieldListFilter),
    )
    exclude = ("is_backlink", "allow_create_backlink", "old_visible")
    search_fields = [
        "urlid",
        "name",
        "citizen_project__name",
        "citizen_project__founder__longname",
        "citizen_project__founder__shortname",
    ]
    ordering = ["name"]

    def project(self, obj):
        return obj.citizen_project.name

    def actor(self, obj):
        return obj.citizen_project.founder.longname


@admin.register(Actor)
class ActorAdmin(EPModelAdmin):
    list_display = ("urlid", "longname", "shortname", "creation_date", "update_date")
    list_filter = (
        "actortype",
        "category",
        "region",
        "visible",
        ("lat", admin.EmptyFieldListFilter),
        ("lng", admin.EmptyFieldListFilter),
        "status",
    )
    search_fields = ["longname", "shortname"]
    ordering = ["longname"]
    filter_horizontal = ("interventionzone",)


@admin.register(Relatedactor)
class RelatedactorAdmin(EPModelAdmin):
    list_display = ("__str__", "actor", "user", "role", "creation_date", "update_date")
    search_fields = [
        "actor__longname",
        "actor__shortname",
        "user__first_name",
        "user__last_name",
        "user__email",
        "role",
    ]
    list_filter = ("role",)


if not getattr(settings, "IS_AMORCE", False):

    @admin.register(Contribution)
    class ContributionAdmin(EPModelAdmin):
        list_display = ("actor", "year", "creation_date", "update_date")
        search_fields = ["actor__longname", "actor__shortname", "year"]
        list_filter = (
            "year",
            "contributionstatus",
        )
        filter_horizontal = ("discount",)

        def get_readonly_fields(self, request, obj=None):
            if obj and obj.contributionstatus in (
                "a_ventiler",
                "valide",
            ):
                return self.readonly_fields + ("amount",)  # type: ignore
            return self.readonly_fields

else:

    admin.site.register(Contribution, EmptyAdmin)
