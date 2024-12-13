"""djangoldp uploader URL Configuration"""

from django.conf import settings
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from djangoldp_ep.views import (ContributionsActorUpdateView,
                                ContributionsCallView,
                                ContributionsReminderView,
                                ContributionsVentilationView,
                                ExportContributions, ExportContributionsAll,
                                GeneratePdfCall, GeneratePdfReceipt,
                                UpdatedSinceProjectsViewset,
                                WaitingMembersActionView,
                                serve_updated_content)

urlpatterns = [
    path(
        "relatedactors/<int:pk>/action/",
        csrf_exempt(WaitingMembersActionView.as_view()),
        name="waitingmembers-action",
    ),
    path(
        "updatedprojects/",
        UpdatedSinceProjectsViewset.urls(model_prefix="updated-projects"),
        name="citizenprojects-updated",
    ),
    re_path(
        r"^updated/(?P<path>.*)", serve_updated_content, name="serve_updated_content"
    ),
]

if not getattr(settings, "IS_AMORCE", False):
    urlpatterns = urlpatterns + [
        path(
            "contributions/call/",
            csrf_exempt(ContributionsCallView.as_view()),
            name="contributions-call",
        ),
        path(
            "contributions/reminder/",
            csrf_exempt(ContributionsReminderView.as_view()),
            name="contributions-reminder",
        ),
        path(
            "contributions/actor_update/",
            csrf_exempt(ContributionsActorUpdateView.as_view()),
            name="contributions-actor-update",
        ),
        path(
            "contributions/ventilation/",
            csrf_exempt(ContributionsVentilationView.as_view()),
            name="contributions-ventilation",
        ),
        path(
            "contributions/call_pdf/<int:pk>/",
            csrf_exempt(GeneratePdfCall.as_view()),
            name="generate_callpdf_fromhtml",
        ),
        path(
            "contributions/receipt_pdf/<int:pk>/",
            csrf_exempt(GeneratePdfReceipt.as_view()),
            name="generate_receiptpdf_fromhtml",
        ),
        path(
            "contributions/csv/",
            csrf_exempt(ExportContributions.as_view()),
            name="export_contributions",
        ),
        path(
            "contributions/csv_all/",
            csrf_exempt(ExportContributionsAll.as_view()),
            name="export_contributions",
        ),
    ]
