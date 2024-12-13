from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_ep.models.__base import baseEPModel


class baseEPNamedModel(baseEPModel):
    name = models.CharField(max_length=255, blank=True, null=True, default="")

    def __str__(self):
        return self.name or self.urlid

    class Meta(baseEPModel.Meta):
        abstract = True
        ordering = ["name"]
        serializer_fields = baseEPModel.Meta.serializer_fields + [
            "name",
        ]
