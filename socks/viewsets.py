from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from .models import Sock, SockPreference
from .serializers import SockSerializer, SockMatchSerializer, SockPreferenceSerializer


class SockViewSet(viewsets.ModelViewSet):
    queryset = Sock.objects.all()
    serializer_class = SockSerializer

    def list(self, request, *args, **kwargs):
        all_socks = self.filter_queryset(self.get_queryset())
        queryset = all_socks.eligible().for_user(request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def mine(self, request, *args, **kwargs):
        my_socks = self.get_queryset().owned_by_user(request.user)
        serializer = self.get_serializer(my_socks, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def match(self, request, pk=None):
        sock = self.get_object()
        serializer = SockMatchSerializer(sock.match)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def preferences(self, request, pk=None):

        data = request.data.copy()

        data['source_sock'] = self.get_object().pk

        serializer = SockPreferenceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class SockPreferenceViewSet(viewsets.ModelViewSet):
    queryset = SockPreference.objects.all()
    serializer_class = SockPreferenceSerializer
