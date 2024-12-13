from .ep_base import EPBasePermission


def is_member(user, obj):
    if not user.is_anonymous:
        related_actor = getattr(obj, "actor", obj)
        related_actor = getattr(obj, "founder", related_actor)
        if hasattr(related_actor, "members"):
            relation_actor = related_actor.members.filter(user=user).first()
            if relation_actor:
                return relation_actor.role
    return False


class EPActorPermission(EPBasePermission):
    def get_permissions(self, user, model, obj=None):
        permission_roles = getattr(model._meta, "permission_roles", {})
        if obj:
            related_actor = getattr(obj, "actor", obj)
            is_member = self.is_member(user, related_actor)
            if is_member in permission_roles:
                return permission_roles[is_member]["perms"]
        return set()

    def has_object_permission(self, request, view, obj):
        if obj:
            is_member = self.is_member(request.user, obj)
            if request.method in ["PATCH", "PUT"]:
                return is_member == "admin"
            else:
                return not not is_member
        return False

    def is_member(self, user, obj):
        return is_member(user, obj)
