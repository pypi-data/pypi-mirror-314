from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Max
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext_lazy as _

from djangoldp_ep.models.actor import *
from djangoldp_ep.models.contribution import *
from djangoldp_ep.models.discount import *
from djangoldp_ep.models.payment_method import *
from djangoldp_ep.models.regional_network import *
from djangoldp_ep.permissions import EPContributionPermission

CONTRIBUTION_CHOICES = [
    ("appel_a_envoye", "Appel à envoyer"),
    ("appel_ok", "Appel envoyé"),
    ("relance", "Relancé"),
    ("a_ventiler", "A ventiler"),
    ("valide", "Validé"),
]


class Contribution(baseEPModel):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Acteur",
        related_name="contributions",
    )
    year = models.IntegerField(
        blank=True, null=True, verbose_name="Année de cotisation"
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
    amount = models.DecimalField(
        blank=True,
        null=True,
        max_digits=7,
        decimal_places=2,
        verbose_name="Montant à payer",
        default=0,
    )
    contributionnumber = models.IntegerField(
        unique=True, blank=True, null=True, verbose_name="Numéro de la cotisation"
    )
    paymentto = models.ForeignKey(
        Regionalnetwork,
        blank=True,
        null=True,
        max_length=250,
        on_delete=models.SET_NULL,
        verbose_name="Paiement à effectuer à",
    )
    paymentmethod = models.ForeignKey(
        Paymentmethod,
        blank=True,
        null=True,
        max_length=50,
        on_delete=models.SET_NULL,
        verbose_name="Moyen de paiement",
    )
    calldate = models.DateField(
        blank=True, null=True, verbose_name="Date du dernier appel"
    )
    paymentdate = models.DateField(
        verbose_name="Date de paiement", blank=True, null=True
    )
    receptdate = models.DateField(
        verbose_name="Date de l'envoi du reçu", blank=True, null=True
    )
    receivedby = models.ForeignKey(
        Regionalnetwork,
        blank=True,
        null=True,
        max_length=250,
        on_delete=models.SET_NULL,
        related_name="%(class)s_requests_created",
        verbose_name="Paiement reçu par",
    )
    contributionstatus = models.CharField(
        choices=CONTRIBUTION_CHOICES,
        max_length=50,
        default="appel_a_envoye",
        blank=True,
        null=True,
        verbose_name="Etat de la cotisation",
    )
    ventilationpercent = models.DecimalField(
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name="pourcentage de ventilation",
    )
    ventilationto = models.ForeignKey(
        Regionalnetwork,
        blank=True,
        null=True,
        max_length=250,
        on_delete=models.SET_NULL,
        related_name="%(class)s_ventilation",
        verbose_name="Bénéficiaire de la ventilation",
    )
    ventilationdate = models.DateField(
        verbose_name="Date de paiement de la part ventilée", blank=True, null=True
    )
    factureventilation = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name="Numéro de facture de la ventilation",
    )
    callcontact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="animateur régional contact",
    )
    discount = models.ManyToManyField(
        Discount, max_length=25, blank=True, verbose_name="Réduction appliquée"
    )
    updatereminderdate = models.DateField(
        blank=True, null=True, verbose_name="Date de dernière demande de mise à jour"
    )

    def __str__(self):
        if self.actor:
            return "%s - %s" % (str(self.actor), self.year)
        else:
            return "%s - %s" % (self.urlid, self.year)

    @property
    def amountincents(self):
        if self.amount is None:
            return 0
        return int(self.amount * 100)

    @classonlymethod
    def _get_next_contribution_number(cls):
        """
        :return: next unique integer to populate the contributionnumber field
        """
        # TODO: https://git.startinblox.com/energie-partagee/djangoldp_ep/issues/26
        # return uuid.uuid4()
        contribution_max_nb = Contribution.objects.aggregate(Max("contributionnumber"))[
            "contributionnumber__max"
        ]

        if contribution_max_nb is None:
            return 1

        return contribution_max_nb + 1

    @classonlymethod
    def get_current_contribution_year(cls):
        return int(date.today().strftime("%Y"))

    @classonlymethod
    def create_annual_contribution(cls, actor):
        now = date.today()
        # payment_date = now + timedelta(30) # 30 days in the future

        c = Contribution(
            actor=actor,
            year=cls.get_current_contribution_year(),
            numberpeople=actor.numberpeople,
            numberemployees=actor.numberemployees,
            turnover=actor.turnover,
            amount=actor.get_next_contribution_amount(),
            contributionnumber=Contribution._get_next_contribution_number(),
            paymentto=actor.regionalnetwork,
        )
        c.save()

    class Meta(baseEPModel.Meta):
        permission_classes = [EPContributionPermission]
        permission_roles = {
            "member": {"perms": set()},
            "admin": {"perms": {"view"}},
        }
        rdf_type = "energiepartagee:contribution"
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "actor",
            "year",
            "numberpeople",
            "numberemployees",
            "turnover",
            "amount",
            "contributionnumber",
            "paymentto",
            "paymentmethod",
            "calldate",
            "paymentdate",
            "receptdate",
            "receivedby",
            "contributionstatus",
            "ventilationpercent",
            "ventilationto",
            "ventilationdate",
            "factureventilation",
            "callcontact",
            "amountincents",
            "updatereminderdate",
        ]
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")
