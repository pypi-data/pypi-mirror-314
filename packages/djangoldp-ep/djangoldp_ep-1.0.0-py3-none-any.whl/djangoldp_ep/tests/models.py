from django.contrib.auth.models import AbstractUser
from djangoldp.permissions import ReadAndCreate, OwnerPermissions
from djangoldp.models import Model


# we have a custom user Model for running in the test envrionment only
class User(AbstractUser, Model):

    class Meta(AbstractUser.Meta, Model.Meta):
        serializer_fields = ["@id", "username", "first_name", "last_name", "email"]
        permission_classes = [ReadAndCreate, OwnerPermissions]
