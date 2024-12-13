from djangoldp_ep.filters import RelatedactorFilterBackend

from .ep_actor import is_member
from .ep_base import EPBasePermission
from .ep_regional_admin import is_regional_admin


class EPRelatedActorPermissions(EPBasePermission):
    filter_backend = RelatedactorFilterBackend

    def get_permissions(self, user, model, obj=None):
        if user.is_anonymous:
            return set()

        if obj:
            membership = is_member(user, obj)
            if is_regional_admin(user, obj) or membership == "admin":
                return {"view", "add", "change", "delete"}
            elif membership == "membre":
                return {"view", "add"}
            elif membership:
                return {"view"}

        from djangoldp_ep.models.region import Region

        if Region.objects.filter(admins=user).exists():
            return {"view", "add", "change", "delete"}

        return {"view", "add"}

    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        if request.user.is_anonymous:
            return False

        if request.method == "POST":
            role = request.data.get("role")
            if role in ("admin", "membre", "refuse"):
                actor_urlid = request.data.get("actor")["@id"]
                if actor_urlid:
                    from djangoldp_ep.models import Actor

                    is_regional_admin = Actor.objects.filter(
                        urlid=actor_urlid, region__admins=request.user
                    ).exists()
                    if is_regional_admin:
                        return True

                    if role == "admin":
                        return request.user.relatedactor_set.filter(
                            actor__urlid=actor_urlid,
                            role__in=("admin"),
                        ).exists()

                    return request.user.relatedactor_set.filter(
                        actor__urlid=actor_urlid,
                        role__in=("admin", "members"),
                    ).exists()

                return False
            elif role is None and request.user.is_authenticated:
                return True

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if obj:
            # Direct permission if the user is the same as the object's user
            if request.user == obj.user:
                if obj.role == "admin":
                    return request.method in ["GET", "PUT", "PATCH", "DELETE", "POST"]
                elif obj.role == "membre" or obj.role is None or obj.role == "":
                    return request.method == "GET"

            # Additional checks for admin/member roles related to the actor
            if hasattr(obj, "actor") and obj.actor is not None:
                if obj.actor.members.filter(user=request.user, role="admin").exists():
                    return request.method in ["GET", "PUT", "PATCH", "DELETE", "POST"]
            return super().has_object_permission(
                request, view, obj
            ) or is_regional_admin(request.user, obj)

        # Default to False if none of the above conditions are met
        return False
