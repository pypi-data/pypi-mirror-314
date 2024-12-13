from djangoldp_ep.filters import ContributionFilterBackend

from .ep_actor import EPActorPermission
from .ep_regional_admin import is_regional_admin


class EPContributionPermission(EPActorPermission):
    filter_backend = ContributionFilterBackend

    def get_permissions(self, user, model, obj=None):
        if user.is_anonymous:
            return set()

        if obj:
            return super().get_permissions(user, model, obj)

        from djangoldp_ep.models.region import Region

        if Region.objects.filter(admins=user).exists():
            return {"view", "add", "change"}

        return {"view"}

    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        if request.user.is_anonymous:
            return False

        if request.method == "POST":
            actor_urlid = request.data.get("actor")["@id"]
            if actor_urlid:
                from djangoldp_ep.models import Actor

                return Actor.objects.filter(
                    urlid=actor_urlid, region__admins=request.user
                ).exists()
            return False

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if obj:
            return super().has_object_permission(
                request, view, obj
            ) or is_regional_admin(request.user, obj)
        return False
