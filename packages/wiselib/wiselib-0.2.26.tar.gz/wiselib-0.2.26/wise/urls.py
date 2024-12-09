from django.urls import path

from wise.internal.views import health_check
from wise.station.views import get_heap_node

urlpatterns = [
    path(
        "health",
        health_check,
        name="health_check",
    ),
    path("station/heap/node", get_heap_node),
]
