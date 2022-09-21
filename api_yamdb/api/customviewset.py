from rest_framework import filters, mixins, viewsets

from .permissions import IsAdmin


class CreateListDelViewCatGenSet(mixins.CreateModelMixin,
                                 mixins.DestroyModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    """Create, delete and list for Genres and Categories model."""

    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
