from .ep_base import EPBasePermission


def is_regional_admin(user, obj):
    if user.is_anonymous:
        return False
    related_region = obj
    if hasattr(obj, "region"):
        # Notice that region object does have an actors key
        related_region = getattr(obj, "region", obj)
    elif hasattr(obj, "actor"):
        related_actor = getattr(obj, "actor", obj)
        related_region = getattr(related_actor, "region", related_actor)
    elif hasattr(obj, "actors"):
        related_actor = getattr(obj, "actors", obj).first()
        related_region = getattr(related_actor, "region", related_actor)
    elif hasattr(obj, "projects"):
        related_project = getattr(obj, "projects", obj).first()
        related_region = getattr(related_project, "region", related_project)
    elif hasattr(obj, "production_sites"):
        related_production_site = getattr(obj, "production_sites", obj).first()
        related_region = getattr(
            related_production_site, "region", related_production_site
        )
    return (
        hasattr(related_region, "admins")
        and related_region.admins.filter(id=user.id).exists()
    )


class EPRegionalAdminPermission(EPBasePermission):
    def get_permissions(self, user, model, obj=None):
        if obj:
            if self.is_regional_admin(user, obj):
                return {"view", "add", "change", "delete"}
            else:
                return set()
        return set()

    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        if view.model.__module__ == "djangoldp_ep.models.region":
            # Regions containers are read only
            if request.method in ["GET", "OPTIONS"]:
                return True
            return False
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if obj:
            return self.is_regional_admin(request.user, obj)
        return False

    def is_regional_admin(self, user, obj):
        return is_regional_admin(user, obj)
