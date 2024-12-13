import pytz
from dateutil import parser
from django.db.models import Q
from rest_framework import filters


class UpdatedSinceFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        updated_since = request.query_params.get("since")
        if not updated_since:
            print("No updated_since parameter", queryset)
            return queryset.none()

        try:
            updated_since = parser.isoparse(updated_since)
        except ValueError:
            print("Invalid updated_since parameter")
            return queryset.none()

        if updated_since.tzinfo is None:
            updated_since = pytz.UTC.localize(updated_since)

        from djangoldp_ep.models import EnergyProduction, ProductionSite

        # Get projects updated or created directly
        projects = queryset.filter(
            Q(update_date__gte=updated_since) | Q(creation_date__gte=updated_since)
        )

        # Get projects with updated or newly created production sites
        production_sites = ProductionSite.objects.filter(
            Q(update_date__gte=updated_since) | Q(creation_date__gte=updated_since)
        )
        projects_from_sites = queryset.filter(production_sites__in=production_sites)

        # Get projects with updated or newly created energy productions
        energy_productions = EnergyProduction.objects.filter(
            Q(update_date__gte=updated_since) | Q(creation_date__gte=updated_since)
        )
        production_sites_from_energy = ProductionSite.objects.filter(
            energy_productions__in=energy_productions
        )
        projects_from_energy = queryset.filter(
            production_sites__in=production_sites_from_energy
        )

        # Combine all queries using | operator to remove duplicates
        all_projects = projects | projects_from_sites | projects_from_energy

        return all_projects.distinct()
