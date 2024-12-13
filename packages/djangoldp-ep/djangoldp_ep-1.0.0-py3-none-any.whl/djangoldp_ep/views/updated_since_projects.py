from djangoldp.views import LDPViewSet

from djangoldp_ep.filters import UpdatedSinceFilterBackend
from djangoldp_ep.models import CitizenProject


class UpdatedSinceProjectsViewset(LDPViewSet):
    model = CitizenProject
    queryset = CitizenProject.objects.none()
    filter_backends = [UpdatedSinceFilterBackend]
