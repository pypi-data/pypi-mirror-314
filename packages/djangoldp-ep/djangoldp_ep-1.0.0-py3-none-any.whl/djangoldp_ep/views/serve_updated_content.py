import pytz
from dateutil import parser
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.urls import resolve
from django.utils import timezone
from djangoldp.serializers import LDPSerializer
from djangoldp.views import JSONLDRenderer
from rest_framework.response import Response


def serve_updated_content(request, path, **kwargs):

    if request.method != "GET":
        return HttpResponseBadRequest()

    match = resolve("/" + path)
    view = match.func.initkwargs
    model = view["model"]

    since = request.GET.get("since")
    if since:
        try:
            updated_since = parser.isoparse(since)
        except Exception:
            return HttpResponseBadRequest()
    else:
        yesterday = timezone.datetime.now(pytz.UTC) - timezone.timedelta(days=1)
        updated_since = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    if updated_since.tzinfo is None:
        updated_since = pytz.UTC.localize(updated_since)

    try:
        queryset = model.objects.filter(update_date__gte=updated_since)
    except Exception:
        return HttpResponseNotFound()

    try:
        meta_args = {
            "model": model,
            "extra_kwargs": {"@id": {"lookup_field": "urlid"}},
            "depth": 0,
            "fields": [
                field
                for field in (model._meta.serializer_fields or ["@id", "update_date"])
                if field not in (model._meta.nested_fields or [])
            ],
        }
        meta_class = type("Meta", (), meta_args)
        custom_serializer = type(LDPSerializer)(
            model._meta.object_name.lower() + "Serializer",
            (LDPSerializer,),
            {"Meta": meta_class},
        )

        serializer = custom_serializer(
            instance=queryset,
            many=True,
            context={"request": request, "view": match.func},
        )
        response = Response(serializer.data, content_type="application/ld+json")
        response.accepted_renderer = JSONLDRenderer()
        response.accepted_media_type = "application/ld+json"
        response.renderer_context = {
            "request": request,
            "view": view,
            "response": serializer.data,
            "kwargs": kwargs,
        }
        return response
    except Exception as e:
        print(e)
        pass

    return HttpResponseNotFound()
