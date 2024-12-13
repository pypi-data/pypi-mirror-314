from datetime import date

import validators
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template import loader
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.views import LDPAPIView, NoCSRFAuthentication
from rest_framework import status
from rest_framework.response import Response

from djangoldp_ep.models.payment_method import Paymentmethod


class ContributionsView(LDPAPIView):
    authentication_classes = (NoCSRFAuthentication,)

    def dispatch(self, request, *args, **kwargs):
        """overriden dispatch method to append some custom headers"""
        response = super(ContributionsView, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get("origin")
        response["Access-Control-Allow-Methods"] = "POST"
        response["Access-Control-Allow-Headers"] = (
            "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
        )
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Accept-Post"] = "application/json"
        response["Accept"] = "*/*"

        if request.user.is_authenticated:
            try:
                response["User"] = request.user.webid()
            except AttributeError:
                pass
        return response

    def contributionMail(self, request, specificdata):
        # Check that we get an array
        if request.method == "POST" and request.data and isinstance(request.data, list):
            for urlid in request.data:
                # Check that the array entries are URLs
                if validators.url(urlid):
                    # Check that the corresponding Actors exists
                    model, instance = Model.resolve(urlid)
                    if instance and instance.actor:
                        if instance.contributionstatus in specificdata["status_before"]:
                            # Modify the contribution status
                            if instance.amount == 0.00:
                                # For given contributions (amount at 0), specific beavior => go directly to the final status
                                instance.contributionstatus = specificdata[
                                    "status_after_given"
                                ]
                                instance.paymentdate = date.today()
                                instance.receivedby = instance.paymentto
                                instance.paymentmethod = Paymentmethod.objects.get(
                                    name="Virement"
                                )
                            else:
                                instance.contributionstatus = specificdata[
                                    "status_after"
                                ]
                            instance.callcontact = request.user
                            instance.calldate = date.today()
                            instance.save()

                        if specificdata["status_before"] == "all":
                            instance.updatereminderdate = date.today()
                            instance.save()
                            for member in instance.actor.members.all():
                                if member.role:
                                    text_message = loader.render_to_string(
                                        specificdata["email_text"],
                                        {
                                            "sender": request.user,
                                            "user": member.user,
                                            "actor": instance.actor,
                                            "contribution": instance,
                                            "uri": request.build_absolute_uri(
                                                "/media/"
                                            ),
                                            "front_url": getattr(
                                                settings,
                                                "INSTANCE_DEFAULT_CLIENT",
                                                "http://localhost",
                                            ),
                                            "back_url": settings.BASE_URL,
                                        },
                                    )
                                    html_message = loader.render_to_string(
                                        specificdata["email_html"],
                                        {
                                            "is_amorce": getattr(
                                                settings, "IS_AMORCE", False
                                            ),
                                            "sender": request.user,
                                            "user": member.user,
                                            "actor": instance.actor,
                                            "contribution": instance,
                                            "uri": request.build_absolute_uri(
                                                "/media/"
                                            ),
                                            "front_url": getattr(
                                                settings,
                                                "INSTANCE_DEFAULT_CLIENT",
                                                "http://localhost",
                                            ),
                                            "back_url": settings.BASE_URL,
                                        },
                                    )
                                    send_mail(
                                        _(
                                            specificdata["email_title"]
                                            + instance.actor.longname
                                        ),
                                        text_message,
                                        settings.DEFAULT_FROM_EMAIL
                                        or "nepasrepondre@energie-partagee.org",
                                        [member.user.email],
                                        fail_silently=False,
                                        html_message=html_message,
                                    )
                            text_message = loader.render_to_string(
                                specificdata["email_text"],
                                {
                                    "sender": request.user,
                                    "user": "",
                                    "actor": instance.actor,
                                    "contribution": instance,
                                    "uri": request.build_absolute_uri("/media/"),
                                    "front_url": getattr(
                                        settings,
                                        "INSTANCE_DEFAULT_CLIENT",
                                        "http://localhost",
                                    ),
                                    "back_url": settings.BASE_URL,
                                },
                            )
                            html_message = loader.render_to_string(
                                specificdata["email_html"],
                                {
                                    "is_amorce": getattr(settings, "IS_AMORCE", False),
                                    "sender": request.user,
                                    "user": "",
                                    "actor": instance.actor,
                                    "contribution": instance,
                                    "uri": request.build_absolute_uri("/media/"),
                                    "front_url": getattr(
                                        settings,
                                        "INSTANCE_DEFAULT_CLIENT",
                                        "http://localhost",
                                    ),
                                    "back_url": settings.BASE_URL,
                                },
                            )
                            msg = EmailMultiAlternatives(
                                _(
                                    specificdata["email_title"]
                                    + instance.actor.longname
                                ),
                                text_message,
                                settings.DEFAULT_FROM_EMAIL
                                or "nepasrepondre@energie-partagee.org",
                                [instance.actor.mail],
                                ["association@energie-partagee.org"],
                            )
                            msg.attach_alternative(html_message, "text/html")
                            # Force raising an error if any
                            msg.send(fail_silently=False)
                        else:
                            text_message = loader.render_to_string(
                                specificdata["email_text"],
                                {
                                    "sender": request.user,
                                    "user": instance.actor.managementcontact,
                                    "actor": instance.actor,
                                    "contribution": instance,
                                    "uri": request.build_absolute_uri("/media/"),
                                    "front_url": getattr(
                                        settings,
                                        "INSTANCE_DEFAULT_CLIENT",
                                        "http://localhost",
                                    ),
                                    "back_url": settings.BASE_URL,
                                },
                            )
                            html_message = loader.render_to_string(
                                specificdata["email_html"],
                                {
                                    "is_amorce": getattr(settings, "IS_AMORCE", False),
                                    "sender": request.user,
                                    "user": instance.actor.managementcontact,
                                    "actor": instance.actor,
                                    "contribution": instance,
                                    "uri": request.build_absolute_uri("/media/"),
                                    "front_url": getattr(
                                        settings,
                                        "INSTANCE_DEFAULT_CLIENT",
                                        "http://localhost",
                                    ),
                                    "back_url": settings.BASE_URL,
                                },
                            )
                            if not instance.amount == 0.00:
                                send_mail(
                                    _(specificdata["email_title"]),
                                    text_message,
                                    settings.DEFAULT_FROM_EMAIL
                                    or "nepasrepondre@energie-partagee.org",
                                    [instance.actor.managementcontact.email],
                                    fail_silently=False,
                                    html_message=html_message,
                                )

            # Questions:
            #   public link to the HTML document ?
            #   Do we want to have it private ?
            response = Response(
                {"content": "This is a success"}, status=status.HTTP_200_OK
            )

            return response

        return Response(status=204)
