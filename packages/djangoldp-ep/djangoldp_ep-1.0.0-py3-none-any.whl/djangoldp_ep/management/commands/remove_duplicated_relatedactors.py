from django.core.management.base import BaseCommand
from django.db.models import Count

from djangoldp_ep.models import Relatedactor


class Command(BaseCommand):
    help = "Removes duplicate Relatedactor entries, keeping the highest priority roles."

    def handle(self, *args, **kwargs):
        role_priority = {"admin": 1, "member": 2, None: 3}

        duplicates = (
            Relatedactor.objects.values("user_id", "actor_id")
            .annotate(total=Count("id"))
            .filter(total__gt=1)
        )

        for duplicate in duplicates:
            related_actors = Relatedactor.objects.filter(
                user_id=duplicate["user_id"], actor_id=duplicate["actor_id"]
            ).order_by("role")

            sorted_actors = sorted(
                related_actors, key=lambda x: role_priority.get(x.role, 99)
            )

            for actor_to_delete in sorted_actors[1:]:
                actor_to_delete.delete()

        self.stdout.write(self.style.SUCCESS("Duplicate entries removed."))
