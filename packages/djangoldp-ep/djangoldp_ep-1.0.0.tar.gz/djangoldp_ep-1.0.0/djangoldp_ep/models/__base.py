from django.db import models
from djangoldp.models import Model
from djangoldp.permissions import AuthenticatedOnly, ReadOnly


class baseEPModel(Model):
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    update_date = models.DateTimeField(
        auto_now=True, verbose_name="Date de dernière mise à jour"
    )

    def __str__(self):
        return self.urlid

    class Meta(Model.Meta):
        abstract = True
        depth = 0
        ordering = ["-update_date"]
        verbose_name = "EP Unknown Object"
        verbose_name_plural = "EP Unknown Objects"

        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
        ]
        nested_fields = []
        rdf_type = "ep:BasicObject"
        permission_classes = [AuthenticatedOnly & ReadOnly]
