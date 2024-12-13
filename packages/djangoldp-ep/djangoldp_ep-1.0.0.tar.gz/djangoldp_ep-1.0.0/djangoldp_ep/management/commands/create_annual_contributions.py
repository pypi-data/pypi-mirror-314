from django.core.management.base import BaseCommand, CommandError

from djangoldp_ep.models import Actor, Contribution


class Command(BaseCommand):
    help = "Calculates the contribution for every actor in the database and creates a Contribution for each, excluding those who have a prior contribution this year"

    def add_arguments(self, parser):
        parser.add_argument(
            "-F",
            action="store_true",
            help="Create a new contribution for every actor in the database, without exception",
        )

    def handle(self, *args, **options):
        count = 0

        for actor in Actor.objects.all():
            # by default do not create a contribution for an actor if one already exists this year
            if (
                options["F"]
                or not actor.contributions.filter(
                    year=Contribution.get_current_contribution_year()
                ).exists()
            ):
                Contribution.create_annual_contribution(actor)
                count += 1

        print("created " + str(count) + " new Contribution records")
