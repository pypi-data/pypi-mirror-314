from django.db.models import Q
from rest_framework_guardian.filters import ObjectPermissionsFilter


#######
# Returns the contributions of the actors the user is admin of
# And the contributions of the region of the user is admin of
# Or all the contributions if the user is superuser
#######
class ContributionFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if (
            not request.user.is_authenticated
            or request.user.is_anonymous
            or queryset.model.__module__
            == "djangoldp_ep.models.zzz__sa_permissions"
        ):
            return queryset.none()
        elif request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(
                Q(
                    Q(actor__members__user=request.user)
                    & Q(actor__members__role="admin")
                )
                | Q(actor__region__admins=request.user)
            )
