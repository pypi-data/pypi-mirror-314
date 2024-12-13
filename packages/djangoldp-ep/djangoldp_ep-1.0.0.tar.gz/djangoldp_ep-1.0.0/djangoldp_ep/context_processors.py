from django.conf import settings


def is_amorce(request):
    return {"is_amorce": getattr(settings, "IS_AMORCE", False)}
