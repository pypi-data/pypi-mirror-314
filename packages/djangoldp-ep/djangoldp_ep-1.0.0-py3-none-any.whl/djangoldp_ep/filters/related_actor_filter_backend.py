from django.db.models import Q
from rest_framework_guardian.filters import ObjectPermissionsFilter


#######
# Returns the related actors on which the user is admin
# Or the complete list if the user is superuser
#######
class RelatedactorFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return queryset.none()
        elif request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(
                Q(actor__members__user=request.user)
                | Q(actor__region__admins=request.user)
            )
