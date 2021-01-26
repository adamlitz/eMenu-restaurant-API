from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Count

from .models import Menu, Dish
from .filters import DateFilter
from .serializers import (
                          MenuSerializer,
                          DishSerializer,
                          FullMenuInfoSerializer,
                          PartialMenuInfoSerializer
                          )


class MenuViewSet(viewsets.ModelViewSet):
    """
    A viewset for listing, editing and deleting menus
    """
    queryset = Menu.objects.annotate(dishes_count=Count('dishes'))
    serializer_class = MenuSerializer

    # Filters config
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_class = DateFilter
    search_fields = ['name', 'created', 'updated']
    ordering_fields = ['name', 'dishes_count']
    ordering = ['name']

    # Permissions config
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        """
        Only non-public API users will see empty menus.
        """
        if not request.user.is_authenticated:
            queryset = self.get_queryset().filter(dishes__isnull=False)
            filtered_queryset = self.filter_queryset(queryset)
        else:
            queryset = self.get_queryset()
            filtered_queryset = self.filter_queryset(queryset)

        serializer = MenuSerializer(filtered_queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Return full information about given menu and corresponding dishes
        """
        instance = self.get_object()

        # Don't show empty menus details in public API
        if not request.user.is_authenticated:
            serializer = PartialMenuInfoSerializer(instance)

            if instance.dishes_count < 1:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = FullMenuInfoSerializer(instance)

        return Response(serializer.data)


class DishViewSet(viewsets.ModelViewSet):
    """
    A viewset for listing, editing and deleting dishes
    """
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    # Permissions config
    permission_classes = [permissions.IsAuthenticated]
