import operator
from functools import reduce

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.template import loader
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from rest_framework.compat import coreapi, coreschema
from rest_framework.filters import BaseFilterBackend


class ConditionalFilter(BaseFilterBackend):
    # The URL query parameter used for the conditional.
    conditional_param = 'conditional'
    conditional_fields = None
    conditional_title = _('Conditional')
    conditional_description = _('Which field to use when conditional the results.')
    template = 'rest_framework/filters/ordering.html'

    def get_conditional(self, request, queryset, view):
        """
        Conditional is set by a comma delimited ?conditional=... query parameter.

        The `conditional` query parameter can be overridden by setting
        the `conditional_param` value on the ConditionalFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        params = request.query_params.get(self.conditional_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            conditional = self.remove_invalid_fields(
                queryset, fields, view, request)
            if conditional:
                return conditional

        # No conditional was included, or all the conditional fields were invalid
        return self.get_default_conditional(view)

    def get_default_conditional(self, view):
        conditional = getattr(view, 'conditional', None)
        if isinstance(conditional, str):
            return (conditional,)
        return conditional

    def get_default_valid_fields(self, queryset, view, context={}):
        # If `conditional_fields` is not specified, then we determine a default
        # based on the serializer class, if one exists on the view.
        if hasattr(view, 'get_serializer_class'):
            try:
                serializer_class = view.get_serializer_class()
            except AssertionError:
                # Raised by the default implementation if
                # no serializer_class was found
                serializer_class = None
        else:
            serializer_class = getattr(view, 'serializer_class', None)

        if serializer_class is None:
            msg = (
                "Cannot use %s on a view which does not have either a "
                "'serializer_class', an overriding 'get_serializer_class' "
                "or 'conditional_fields' attribute."
            )
            raise ImproperlyConfigured(msg % self.__class__.__name__)

        model_class = queryset.model
        model_property_names = [
            # 'pk' is a property added in Django's Model class, however it is valid for conditional.
            attr for attr in dir(model_class) if isinstance(getattr(model_class, attr), property) and attr != 'pk'
        ]

        return [
            (field.source.replace('.', '__') or field_name, field.label)
            for field_name, field in serializer_class(context=context).fields.items()
            if (
                not getattr(field, 'write_only', False) and
                not field.source == '*' and
                field.source not in model_property_names
            )
        ]

    def get_valid_fields(self, queryset, view, context={}):
        valid_fields = getattr(view, 'conditional_fields', self.conditional_fields)

        if valid_fields is None:
            # Default to allowing filtering on serializer fields
            return self.get_default_valid_fields(queryset, view, context)

        elif valid_fields == '__all__':
            # View explicitly allows filtering on any model field
            valid_fields = [
                (field.name, field.verbose_name) for field in queryset.model._meta.fields
            ]
            valid_fields += [
                (key, key.title().split('__'))
                for key in queryset.query.annotations
            ]
        else:
            valid_fields = [
                (item, item) if isinstance(item, str) else item
                for item in valid_fields
            ]

        return valid_fields

    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = [item[0] for item in self.get_valid_fields(
            queryset, view, {'request': request})]

        def term_valid(term):
            if term.startswith("-"):
                term = term[1:]
            return term in valid_fields

        return [term for term in fields if term_valid(term)]

    def filter_queryset(self, request, queryset, view):
        conditional = self.get_conditional(request, queryset, view)

        if conditional:
            conditions = []
            for condition in conditional:
                value = True
                if condition[0] == '-':
                    value = False
                    condition = condition[1:]
                conditions.append(models.Q(**{'{}__exact'.format(condition): value}))
            queryset = queryset.filter(reduce(operator.and_, conditions))
        return queryset

    def get_template_context(self, request, queryset, view):
        current = self.get_conditional(request, queryset, view)
        current = None if not current else current[0]
        options = []
        context = {
            'request': request,
            'current': current,
            'param': self.conditional_param,
        }
        for key, label in self.get_valid_fields(queryset, view, context):
            options.append((key, '%s - %s' % (label, _('true'))))
            options.append(('-' + key, '%s - %s' % (label, _('false'))))
        context['options'] = options
        return context

    def to_html(self, request, queryset, view):
        template = loader.get_template(self.template)
        context = self.get_template_context(request, queryset, view)
        return template.render(context)

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.conditional_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.conditional_title),
                    description=force_str(self.conditional_description)
                )
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': self.conditional_param,
                'required': False,
                'in': 'query',
                'description': force_str(self.conditional_description),
                'schema': {
                    'type': 'string',
                },
            },
        ]
