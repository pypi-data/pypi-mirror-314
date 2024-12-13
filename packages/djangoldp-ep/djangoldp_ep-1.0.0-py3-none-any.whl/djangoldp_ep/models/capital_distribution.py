from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.permissions import InheritPermissions

from djangoldp_ep.models.__base import baseEPModel
from djangoldp_ep.models.actor import Actor


class CapitalDistribution(baseEPModel):
    actor = models.OneToOneField(
        Actor,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Acteur",
        related_name="capital_distribution",
    )
    individuals_count = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre d'actionnaires personnes physiques"
    )
    individuals_capital = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Montant en capital personnes physiques",
    )
    other_funds_capital = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres fonds propres personnes physiques",
    )
    individuals_count_resident = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre d'actionnaires résidents"
    )
    other_ess_orgs_capital = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Montant en capital ESS",
    )
    other_ess_orgs_other_funds = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres fonds propres ESS",
    )
    communities_count = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre de collectivités"
    )
    communities_capital = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Montant en capital collectivités",
    )
    communities_other_funds = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres fonds propres collectivités",
    )
    neighboring_communities_count = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre de collectivités résidentes"
    )
    other_private_orgs_capital = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Montant en capital autres acteurs",
    )
    other_private_orgs_other_funds = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Autres fonds propres autres acteurs",
    )

    @property
    def total_amount(self):
        compute = 0

        if self.individuals_capital:
            compute += self.individuals_capital
        if self.other_funds_capital:
            compute += self.other_funds_capital
        if self.other_ess_orgs_capital:
            compute += self.other_ess_orgs_capital
        if self.other_ess_orgs_other_funds:
            compute += self.other_ess_orgs_other_funds
        if self.communities_capital:
            compute += self.communities_capital
        if self.communities_other_funds:
            compute += self.communities_other_funds
        if self.other_private_orgs_capital:
            compute += self.other_private_orgs_capital
        if self.other_private_orgs_other_funds:
            compute += self.other_private_orgs_other_funds

        for shareholder in self.shareholders.all():
            if shareholder.capital_amount:
                compute += shareholder.capital_amount
            if shareholder.other_funds_amount:
                compute += shareholder.other_funds_amount
            if shareholder.relay_investment:
                compute += shareholder.relay_investment

        return compute

    @property
    def total_capital(self):
        compute = 0

        if self.individuals_capital:
            compute += self.individuals_capital
        if self.other_ess_orgs_capital:
            compute += self.other_ess_orgs_capital
        if self.communities_capital:
            compute += self.communities_capital
        if self.other_private_orgs_capital:
            compute += self.other_private_orgs_capital

        for shareholder in self.shareholders.all():
            if shareholder.capital_amount:
                compute += shareholder.capital_amount

        return compute

    @property
    def total_other_funds(self):
        compute = 0

        if self.other_funds_capital:
            compute += self.other_funds_capital
        if self.other_ess_orgs_other_funds:
            compute += self.other_ess_orgs_other_funds
        if self.communities_other_funds:
            compute += self.communities_other_funds
        if self.other_private_orgs_other_funds:
            compute += self.other_private_orgs_other_funds

        for shareholder in self.shareholders.all():
            if shareholder.other_funds_amount:
                compute += shareholder.other_funds_amount

        return compute

    @property
    def individuals_capital_percentage(self):
        if self.individuals_capital:
            return round(self.individuals_capital / self.total_capital * 100, 2)
        return 0

    @property
    def other_funds_capital_percentage(self):
        if self.other_funds_capital:
            return round(self.other_funds_capital / self.total_other_funds * 100, 2)
        return 0

    @property
    def other_ess_orgs_capital_percentage(self):
        if self.other_ess_orgs_capital:
            return round(self.other_ess_orgs_capital / self.total_capital * 100, 2)
        return 0

    @property
    def other_ess_orgs_other_funds_percentage(self):
        if self.other_ess_orgs_other_funds:
            return round(
                self.other_ess_orgs_other_funds / self.total_other_funds * 100, 2
            )
        return 0

    @property
    def communities_capital_percentage(self):
        if self.communities_capital:
            return round(self.communities_capital / self.total_capital * 100, 2)
        return 0

    @property
    def communities_other_funds_percentage(self):
        if self.communities_other_funds:
            return round(self.communities_other_funds / self.total_other_funds * 100, 2)
        return 0

    @property
    def other_private_orgs_capital_percentage(self):
        if self.other_private_orgs_capital:
            return round(self.other_private_orgs_capital / self.total_capital * 100, 2)
        return 0

    @property
    def other_private_orgs_other_funds_percentage(self):
        if self.other_private_orgs_other_funds:
            return round(
                self.other_private_orgs_other_funds / self.total_other_funds * 100, 2
            )
        return 0

    class Meta(baseEPModel.Meta):
        permission_classes = [InheritPermissions]
        inherit_permissions = ["actor"]
        rdf_type = "energiepartagee:capital_distribution"
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "individuals_count",
            "individuals_capital",
            "other_funds_capital",
            "individuals_count_resident",
            "other_ess_orgs_capital",
            "other_ess_orgs_other_funds",
            "communities_count",
            "communities_capital",
            "communities_other_funds",
            "neighboring_communities_count",
            "other_private_orgs_capital",
            "other_private_orgs_other_funds",
            "shareholders",
            "total_capital",
            "total_other_funds",
            "individuals_capital_percentage",
            "other_funds_capital_percentage",
            "other_ess_orgs_capital_percentage",
            "other_ess_orgs_other_funds_percentage",
            "communities_capital_percentage",
            "communities_other_funds_percentage",
            "other_private_orgs_capital_percentage",
            "other_private_orgs_other_funds_percentage",
        ]
        nested_fields = ["shareholders"]
        verbose_name = _("Distribution du capital")
        verbose_name_plural = _("Distribution des capitaux")
        depth = 1
        static_version = 1

    def __str__(self):
        if self.actor:
            return str(self.actor)
        else:
            return self.urlid
