from rest_framework import viewsets

from . import mixins


class FieldsModelViewSet(mixins.ListFieldsModelMixin,
                         viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass
