from rest_framework.response import Response


class ListFieldsModelMixin:
    """
    List a queryset with selected fields.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        fields = request.query_params.get('fields')
        if fields:
            fields = fields.split(',')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=fields)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, fields=fields)
        return Response(serializer.data)
