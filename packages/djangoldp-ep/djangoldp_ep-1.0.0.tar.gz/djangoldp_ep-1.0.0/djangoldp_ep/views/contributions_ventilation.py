import validators
from djangoldp.models import Model
from rest_framework import status
from rest_framework.response import Response

from djangoldp_ep.models.contribution import CONTRIBUTION_CHOICES
from djangoldp_ep.views.contributions import ContributionsView


class ContributionsVentilationView(ContributionsView):
    def post(self, request):
        # from djangoldp_ep.models import CONTRIBUTION_CHOICES

        if request.data:
            # Check parameters
            data_expected = [
                "ventilationpercent",
                "ventilationto",
                "ventilationdate",
                "factureventilation",
                "contributions",
            ]

            if not all(parameter in request.data.keys() for parameter in data_expected):
                missing_params = [
                    parameter
                    for parameter in data_expected
                    if parameter not in request.data.keys()
                ]
                return Response(
                    "Invalid parameters: {} missing".format(", ".join(missing_params)),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check regional network
            ventilationto_urlid = request.data["ventilationto"]["@id"]
            if validators.url(ventilationto_urlid):
                model, instance = Model.resolve(ventilationto_urlid)
                if instance:
                    ventilationto = instance
                else:
                    return Response(
                        "Regional network does not exist in DB",
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Check contributions
            contribution_list = []
            for contrib_urlid in request.data["contributions"]:
                if validators.url(contrib_urlid):
                    model, instance = Model.resolve(contrib_urlid)
                    if instance:
                        contribution_list.append(instance)
                    else:
                        return Response(
                            "Contribution {} does not exist in DB".format(
                                contrib_urlid
                            ),
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            # Ventilate
            for contrib in contribution_list:
                contrib.ventilationpercent = request.data["ventilationpercent"]
                contrib.ventilationto = ventilationto
                contrib.ventilationdate = request.data["ventilationdate"]
                contrib.factureventilation = request.data["factureventilation"]
                contrib.contributionstatus = CONTRIBUTION_CHOICES[4][0]
                contrib.save()

            # Send response
            response = Response(
                {"content": "This is a success"}, status=status.HTTP_200_OK
            )

            return response

        return Response(status=204)
