from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from wise.station.registry import station_registry


@api_view(["GET"])
def get_heap_node(request):
    publisher_name = request.query_params.get("name")
    index = request.query_params.get("index")
    if not publisher_name or not index:
        return Response(
            {"error": "name and index are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    publisher = None
    for p in station_registry.publishers:
        if p.name == publisher_name:
            publisher = p
            break

    if not publisher or not publisher.enable_heap:
        return Response(
            {"error": "publisher not found or heap disabled"},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        publisher.get_heap_index_message(int(index)),
        status=status.HTTP_200_OK,
    )
