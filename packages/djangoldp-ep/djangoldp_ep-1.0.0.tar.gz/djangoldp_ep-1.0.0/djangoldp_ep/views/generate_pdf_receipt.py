import validators
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from djangoldp.models import Model

from djangoldp_ep.models.contribution import Contribution
from djangoldp_ep.views.utils import render_to_pdf


class GeneratePdfReceipt(DetailView):
    model = Contribution
    template_name = "pdf/contribution_receipt.html"

    def get(self, request, *args, **kwargs):
        instance = Contribution.objects.get(id=kwargs["pk"])

        if instance:
            context = {
                "contribution": instance,
                "uri": request.build_absolute_uri("/media/"),
            }
            pdf = render_to_pdf(self.template_name, context)

            if pdf:
                response = HttpResponse(
                    pdf, content_type="application/pdf; charset=utf-8"
                )
                filename = "Recu de cotisation.pdf"
                content = "inline; filename=%s" % (filename)
                response["Content-Disposition"] = content
                return response

        return HttpResponse("Not Found")

    def post(self, request, *args, **kwargs):
        # try:
        #     from djangoldp_ep.models import Contribution
        # except (get_user_model().DoesNotExist, KeyError):
        #     pass

        # Check that the array entries are URLs
        if validators.url(request.data.urlid):
            # Check that the corresponding Actors exists
            model, instance = Model.resolve(request.data.urlid)

            context = {
                "number": instance.contributionnumber,
                "actor": instance.actor.name,
            }
            pdf = render_to_pdf(self.template_name, context)

            if pdf:
                response = HttpResponse(
                    pdf, content_type="application/pdf; charset=utf-8"
                )
                filename = "Recu de cotisation.pdf"
                content = "inline; filename=%s" % (filename)
                response["Content-Disposition"] = content
                return response

        return HttpResponse("Not Found")
