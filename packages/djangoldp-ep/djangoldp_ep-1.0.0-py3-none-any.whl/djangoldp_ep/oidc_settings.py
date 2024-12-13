from django.utils.translation import gettext_lazy as _
from oidc_provider.lib.claims import ScopeClaims


class ActorsScopeClaims(ScopeClaims):
    info_moncompte = (
        _("Moncompte"),
        _(
            "This is the custom claim providing info on all EnergiePartagee information associated with the user."
        ),
    )

    def scope_moncompte(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        dic = {}

        if self.user.is_authenticated:
            # Get list of related actors of current user
            from djangoldp_ep.models.actor import Actor
            from djangoldp_ep.models.related_actor import Relatedactor

            if self.user.is_superuser:
                return {"membership": "inactive", "regional_admin": "enabled"}

            user_actors_id = Relatedactor.get_user_actors_id(
                user=self.user, role=["admin", "membre"]
            )

            # Get membership status of the actors
            active_actors = Actor.objects.filter(
                id__in=user_actors_id,
                renewed=True,
            )

            if active_actors.exists():
                dic = {
                    "membership": "active",
                }
            else:
                dic = {
                    "membership": "inactive",
                }

            # Check if user is associated with a region as is_admin
            from djangoldp_ep.models.region import Region

            region = Region.objects.filter(admins=self.user)

            if region.exists():
                dic["regional_admin"] = "enabled"
            else:
                dic["regional_admin"] = "disabled"

        return dic

    # If you want to change the description of the profile scope, you can redefine it.
    info_profile = (
        _("Profile"),
        _("Another description."),
    )

    def scope_profile(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        dic = {}

        if self.user.is_authenticated:
            dic = {
                "username": self.user.username,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "name": self.user.get_full_name(),
            }

        return dic
