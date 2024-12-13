from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_ep.models.college import *


class Regionalnetwork(baseEPNamedModel):
    address = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Adresse"
    )
    postcode = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="Code Postal"
    )
    city = models.CharField(max_length=250, blank=True, null=True, verbose_name="Ville")
    colleges = models.ManyToManyField(
        College, blank=True, max_length=50, verbose_name="Collège"
    )
    code = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Code du réseau"
    )
    logo = models.ImageField(blank=True, null=True, verbose_name="Logo")
    siren = models.CharField(max_length=20, blank=True, null=True, verbose_name="SIRET")
    usercontact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="contact",
    )
    bank = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Banque"
    )
    iban = models.CharField(max_length=35, blank=True, null=True, verbose_name="IBAN")
    bic = models.CharField(max_length=15, blank=True, null=True, verbose_name="BIC")
    orderpayment = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Ordre de paiement"
    )
    addresspayment = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Adresse de paiement"
    )
    postcodepayment = models.CharField(
        max_length=5, blank=True, null=True, verbose_name="Code Postal de paiement"
    )
    citypayment = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Ville de paiement"
    )
    signature = models.ImageField(blank=True, null=True, verbose_name="Signature")
    mandat = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Mandat du responsable légal",
    )
    respname = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Nom du responsable légal"
    )
    respfirstname = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Prénom du responsable légal"
    )
    nationale = models.BooleanField(
        verbose_name="Réseau National", blank=True, null=True, default=False
    )

    class Meta(baseEPNamedModel.Meta):
        rdf_type = "energiepartagee:regionalnetwork"
        nested_fields = ["colleges"]
        serializer_fields = baseEPNamedModel.Meta.serializer_fields + [
            "address",
            "postcode",
            "city",
            "colleges",
            "code",
            "logo",
            "siren",
            "usercontact",
            "bank",
            "iban",
            "bic",
            "orderpayment",
            "postcodepayment",
            "citypayment",
            "signature",
            "mandat",
            "respname",
            "respfirstname",
            "nationale",
        ]
        verbose_name = _("Réseau régional")
        verbose_name_plural = _("Réseaux régionaux")
