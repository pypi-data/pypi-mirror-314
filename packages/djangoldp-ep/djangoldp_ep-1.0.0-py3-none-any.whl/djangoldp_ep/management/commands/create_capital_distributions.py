from django.core.management.base import BaseCommand

from djangoldp_ep.models import Actor, CapitalDistribution


class Command(BaseCommand):
    help = "Ensure that every actor has its CapitalDistribution"

    def handle(self, *args, **options):
        count = 0

        for actor in Actor.objects.all():
            CapitalDistribution.objects.get_or_create(actor=actor)
            count += 1

        print("Checked " + str(count) + " Actors records")
