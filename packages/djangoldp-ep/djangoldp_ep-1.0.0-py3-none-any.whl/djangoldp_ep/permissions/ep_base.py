from djangoldp.permissions import LDPBasePermission


class EPBasePermission(LDPBasePermission):
    def get_permissions(self, user, model, obj=None):
        if user.is_superuser:
            return {"view", "add", "change", "delete"}

        return set()
