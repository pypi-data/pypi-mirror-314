import json
import logging
import re
from json import JSONDecodeError

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import (
    FieldDoesNotExist,
    FieldError,
    ValidationError,
)
from django.db import IntegrityError, transaction
from django.db.models import ForeignKey, Model, Q
from django.db.models.fields import AutoFieldMixin
from django.shortcuts import redirect
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views import View

import dill

from pfx.pfxcore import __PFX_VIEWS__
from pfx.pfxcore.apidoc import ModelListSchema, ModelSchema, Schema, Tag
from pfx.pfxcore.decorator import rest_api
from pfx.pfxcore.exceptions import (
    APIError,
    ForbiddenError,
    JsonErrorAPIError,
    ModelValidationAPIError,
    NotFoundError,
    UnauthorizedError,
)
from pfx.pfxcore.fields import MediaField
from pfx.pfxcore.http import JsonResponse
from pfx.pfxcore.models import JSONReprMixin, UserFilteredQuerySetMixin
from pfx.pfxcore.shortcuts import class_key, f, get_bool, get_int, get_object
from pfx.pfxcore.storage.s3_storage import StorageException

from . import parameters
from .fields import VF
from .fields import FieldType as FT
from .fields import ViewField

logger = logging.getLogger(__name__)


# HTTP 404 handler
def resource_not_found(request, exception):
    return NotFoundError().response


class ModelMixin():
    """Base mixin for a model view."""

    #: The model class, must be defined on concrete classes.
    model = None
    #: The default fields list.
    fields = []

    def apply_user_filter(self, qs):
        """Apply filters to restrict the queryset according to user rights.

        :param qs: The queryset
        :type qs: :class:`django.db.models.QuerySet`
        :returns: The filtered queryset
        :rtype: :class:`django.db.models.QuerySet`
        """
        if isinstance(qs, UserFilteredQuerySetMixin):
            return qs.user(self.request.user)
        if (hasattr(settings, 'PFX_FORCE_USER_FILTERED_QUERYSET') and
                settings.PFX_FORCE_USER_FILTERED_QUERYSET):
            raise Exception("The queryset must be a UserFilteredQuerySetMixin")
        return qs

    def get_queryset(self, select_related=None, prefetch_related=None):
        """Get the queryset for the view model.

        The returned queryset is filtered according to user rights.

        :param select_related: Arguments for queryset select_related
        :type select_related: :class:`list[str]`
        :param prefetch_related: Arguments for queryset prefetch_related
        :type prefetch_related: :class:`list[str]`
        :returns: The queryset
        :rtype: :class:`django.db.models.QuerySet`
        """
        qs = self.apply_user_filter(self.model._default_manager.all())
        if select_related:
            qs = qs.select_related(*select_related)
        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)
        return qs

    def get_object(self, **kwargs):
        """Get a single object matching the given keyword arguments.

        :param \\**kwargs: Keyword arguments
        :returns: A view model instance
        """
        return get_object(self.get_queryset(
            select_related=self.get_fields_select_related(),
            prefetch_related=self.get_fields_prefetch_related()), **kwargs)

    def get_related_queryset(
            self, related_model, select_related=None, prefetch_related=None):
        """Get a queryset for another related model.

        The returned queryset is filtered according to user rights.

        :param related_model: An arbitrary DJango model.
        :param select_related: Arguments for queryset select_related
        :type select_related: :class:`list[str]`
        :param prefetch_related: Arguments for queryset prefetch_related
        :type prefetch_related: :class:`list[str]`
        :returns: The queryset
        :rtype: :class:`django.db.models.QuerySet`
        """
        qs = self.apply_user_filter(related_model._default_manager.all())
        if select_related:
            qs = qs.select_related(*select_related)
        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)
        return qs

    def get_list_queryset(self, select_related=None, prefetch_related=None):
        """Get a queryset for the view model dedicated for lists.

        This method returns the same result as :code:`get_queryset` and is
        defined only to allow it to be overloaded in order to customize
        the queryset for lists.

        :param select_related: Arguments for queryset select_related
        :type select_related: :class:`list[str]`
        :param prefetch_related: Arguments for queryset prefetch_related
        :type prefetch_related: :class:`list[str]`
        :returns: The queryset
        :rtype: :class:`django.db.models.QuerySet`
        """
        return self.get_queryset(select_related, prefetch_related)

    @classmethod
    def _process_fields(cls, fields):
        if not fields:
            return {
                _f.name: ViewField.from_model_field(_f.name, _f)
                for _f in cls.model._meta.fields}

        def _field(e):
            if isinstance(e, ViewField):
                field = e
            elif isinstance(e, VF):
                field = e.to_field(cls.model)
            else:
                field = ViewField.from_name(cls.model, e)
            return field.alias, field

        return dict(_field(e) for e in fields)

    @classmethod
    def get_fields(cls):
        """Return the processed field list.

        Return a list of :class:`ViewField` built from :code:`cls.fields`.

        The result is cached.

        :returns: The fields list
        :rtype: :class:`list[pfx.pfxcore.views.ViewField]`
        """
        return dill.loads(cache.get_or_set(
            class_key(cls, 'fields'),
            lambda: dill.dumps(cls._process_fields(cls.fields)), None))

    @classmethod
    def get_fields_select_related(cls):
        """:meta private: Undocumented because it must be changed."""
        return cache.get_or_set(
            class_key(cls, 'fields', 'select_related'),
            lambda: set([
                _f for field in cls.get_fields().values()
                for _f in field.select_related]),
            None)

    @classmethod
    def get_fields_prefetch_related(cls):
        """:meta private: Undocumented because it must be changed."""
        return cache.get_or_set(
            class_key(cls, 'fields', 'prefetch_related'),
            lambda: set([
                _f for field in cls.get_fields().values()
                for _f in field.prefetch_related]),
            None)

    @property
    def model_name(self):
        """Get the model verbose name.

        :returns: The model
        :rtype: :class:`str`
        """
        return self.model._meta.verbose_name

    @property
    def format_date(self):
        """:meta private: Undocumented because it must be changed."""
        return get_bool(self.request.GET, 'date_format')

    def message_response(self, message, **kwargs):
        """Build a message JSON response.

        :param message: A message
        :type message: str
        :param \\**kwargs: Other JSON values to add to the response.
        :returns: The response
        :rtype: :class:`pfx.pfxcore.http.JsonResponse`
        """
        return JsonResponse(dict(message=message, **kwargs))

    def delete_object(self, obj):
        """Delete a model object instance.

        Raise an :class:`APIError` for :class:`IntegrityError`.
        If the exception is not catch,
        A JSON HTTP response is returned by the API call.

        :param obj: The object to delete
        """
        try:
            with transaction.atomic():
                obj.delete()
        except IntegrityError as e:
            logger.debug("IntegrityError: %s", e)
            raise APIError(f(_(
                "{obj} cannot be deleted because "
                "it is referenced by other objects."), obj=obj))

    @classmethod
    def get_apidoc_tags(cls):
        """Get the tags for ApiDoc.
        """
        return cls.tags or [
            Tag(str(cls.model._meta.verbose_name))]


class ModelResponseMixin(ModelMixin):
    """Extension of :class:`ModelMixin` to manage object responses."""
    #: The response schema for meta service.
    meta_schema = None
    #: The model schema.
    model_schema = None
    #: The create response schema.
    model_create_schema = None
    #: The update response schema.
    model_update_schema = None
    #: The message response schema.
    model_message_schema = None

    def serialize_object(self, obj, **fields):
        """Serialize an object into a python :class:`dict`.

        If the object is a :class:`JSONReprMixin`,
        use the :code:`json_repr` method.
        Otherwise return a default representation.

        :param obj: The object
        :param \\**fields: Other values to add to the representation
        :returns: The object representation
        :rtype: :class:`dict`
        """
        if isinstance(obj, JSONReprMixin):
            vals = obj.json_repr()
        else:
            vals = dict(
                pk=obj.pk,
                resource_name=str(obj))
        vals.update(fields)
        return vals

    def response(self, o, **meta):
        """Build a :class:`JsonResponse` from an object instance.

        :param o: The object instance
        :param \\**meta: Meta values to add to the response
        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        """
        return JsonResponse(self.serialize_object(o, **{
            _f.alias: _f.to_json(o, self.format_date)
            for _f in self.get_fields().values()}, meta=meta))

    def validate(self, obj, created=False, **kwargs):
        """Validate an object instance.

        can be overridden to customize validation on a given view
        (apart from object validation).

        :param o: The object instance to validate
        :param created: If object instance is created
        :param \\**kwargs: Additional arguments for :code:`full_clean`
        """
        obj.full_clean(**kwargs)

    def is_valid(self, obj, created=False, rel_data=None):
        """Persist an object instance changes and build default response.

        The default response contains the serialized instance after save and
        a text message.

        You can use :code:`rel_data` to pass values to set on related fields
        after instance is persisted (to avoid errors if the instance does
        not exists in database).

        :param obj: The object instance
        :param created: If object instance is created
        :param rel_data: Values to set on related fields
        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        """
        if rel_data:
            with transaction.atomic():
                obj.save()
                for k, v in rel_data.items():
                    getattr(obj, k).set(v)
        else:
            obj.save()
        message = (
                created and
                _("{model} {obj} created.") or
                _("{model} {obj} updated."))
        object = self.get_object(pk=obj.pk)
        return self.response(
            object, message=f(
                message, model=self.model_name, obj=object))

    def is_invalid(self, obj, errors):
        """Build a 422 response for invalid object instance.

        :param obj: The object instance
        :param errors: The validations errors
        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        """
        return JsonResponse(errors, status=422)

    def object_meta(self):
        """Build metadata for the view model.

        :returns: The metadata
        :rtype: :class:`dict`
        """
        meta = {}
        defaults = {} if self.request.GET.keys() else dict(fields=True)
        if get_bool(self.request.GET, 'fields', defaults.get('fields')):
            meta['fields'] = cache.get_or_set(
                class_key(self.__class__, 'meta', 'fields'),
                lambda: {n: f.meta() for n, f in self.get_fields().items()},
                None)
        return meta

    @rest_api(
        "/meta", method="get", response_schema='meta_schema', priority_doc=20)
    def get_meta(self, *args, **kwargs):
        """Entrypoint for :code:`GET /meta` route.

        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        get:
            summary: Get {model} metadata
        """
        return JsonResponse(self.object_meta())

    @classmethod
    def generate_schemas(cls):
        """Generate schemas for the class.
        """
        from .fields import FieldType
        super().generate_schemas()
        cls.meta_schema = Schema('form_meta', "Meta", properties=dict(
            fields=dict(
                type='array', items=dict(type='object', properties=dict(
                    name=dict(type='string'),
                    type=dict(
                        type='string',
                        enum=list(FieldType.APIDOC_FIELD_BINDING.keys())),
                    choices=dict(
                        type='array', items=dict(type='string'),
                        example=["value1", "value2"]),
                    readonly=dict(type='object', properties=dict(
                        post=dict(type='boolean'),
                        put=dict(type='boolean'))),
                    required=dict(type='boolean'))),
                description="List of fields.")))
        cls.model_schema = ModelSchema(cls.model, cls.get_fields())
        cls.model_create_schema = ModelSchema(
            cls.model, cls.get_fields(), mode='create')
        cls.model_update_schema = ModelSchema(
            cls.model, cls.get_fields(), mode='update')
        cls.model_message_schema = ModelSchema(
            cls.model, cls.get_fields(), dict(message=dict(type='string')))

    @classmethod
    def get_apidoc_schemas(cls):
        """Get schemas for the class.

        :returns: The schemas list
        :rtype: :class:`list[pfx.pfxcore.apidoc.Schema]`
        """
        return super().get_apidoc_schemas() + [
            cls.meta_schema, cls.model_schema, cls.model_create_schema,
            cls.model_update_schema, cls.model_message_schema]


class BodyMixin:
    """Base mixin for request body management."""

    def deserialize_body(self):
        """Return the request body as a python :class:`dict`.
        """
        try:
            return json.loads(self.request.body)
        except JSONDecodeError as e:
            raise JsonErrorAPIError(e)

    def body_to_model(
            self, model: Model, validate=True, fields=None, **kwargs):
        """Return a new model instance built with request body.

        :param model: The model to instantiate
        :param validate: Activate validation
        :param \\**kwargs: The optional arguments for `full_clean`
        :rtype: :class:`django.db.models.Model`
        """
        if fields is None:
            fields = [
                _f.name for _f in model._meta.get_fields()
                if not isinstance(_f, AutoFieldMixin)]
        obj = model(**{
            k: v for k, v in self.deserialize_body().items() if k in fields})
        if validate:
            try:
                obj.full_clean(**kwargs)
            except ValidationError as e:
                raise ModelValidationAPIError(e)
        return obj


class ModelBodyMixin(BodyMixin, ModelMixin):
    """Extension mixin to process object in body."""

    def get_model_data(self, obj, data, created):
        """Process data for object update or creation.

        Return a tuple of data and rel_data. The returned data contains
        only fields that can be modified in this context (create or update).

        Values are deserialized according to field definition. If the field
        il a related object list, the value is set in rel_data.

        :returns: The data and rel_data
        :rtype: :class:`tuple(dict, dict)`
        """
        fields = self.get_fields()

        def can_write(fname):
            if fname not in fields:
                return False
            if fields[fname].is_readonly(created=created):
                logger.warning(
                    "Field %s is ignored because it is readonly on view %s",
                    fname, self.__class__.__name__)
                return False
            return True

        res = {}
        res_rel = {}
        for k, v in data.items():
            if can_write(k):
                mk, mv = fields[k].to_model_value(v, self.get_related_queryset)
                if fields[k].field_type == FT.ModelObjectList:
                    res_rel[mk] = mv
                else:
                    res[mk] = mv
        return res, res_rel

    def set_values(self, obj, **values):
        """Set object fields value.

        :param obj: The object to update
        :param \\**values: The values to set
        """
        for fname, value in values.items():
            setattr(obj, fname, value)


class ListRestViewMixin(ModelResponseMixin):
    """Extension mixin to manage object list response."""

    class Subset:
        """Subset enum."""
        NONE = 'none'
        PAGINATION = 'pagination'
        OFFSET = 'offset'

    #: The fields for list responses.
    list_fields = []
    #: The filters available for list responses.
    filters = []
    #: The schema for list metadata.
    meta_list_schema = None
    #: The schema for responses.
    model_list_schema = None

    def get_list_fields(self):
        """Return the processed field list for lists.

        Return a list of :class:`ViewField` built from :code:`cls.list_fields`
        (or :code:`cls.fields` if :code:`cls.list_fields` is empty).

        the result is cached on the class, to ensure that the build
        is carried out no more than once per request.

        :returns: The fields list
        :rtype: :class:`list[pfx.pfxcore.views.ViewField]`
        """
        if not hasattr(self, '_list_fields'):
            self._list_fields = dill.loads(cache.get_or_set(
                class_key(self.__class__, 'list_fields'),
                lambda: dill.dumps(self._process_fields(
                    self.list_fields or self.fields)), None))
        return self._list_fields

    def get_list_meta_filters(self):
        """Return the filters metadata for lists.

        :returns: The filters metadata generator
        :rtype: :class:`generator`
        """
        for _f in self.filters:
            yield _f.meta

    def search_filter(self, search):  # pragma: no cover
        """Return the django filters for the default text search.

        This default implementation returns empty filters, which will always
        produce empty results. This method is designed to be implemented
        by the view to be customized.

        :returns: The django filters
        :rtype: :class:`django.db.models.Q`
        """
        return Q()

    def orderable_fields(self, model, models=None):
        """:meta private: Undocumented because it must be changed/removed."""
        models = models or [model]
        new_models = models + [
            field.related_model for field in model._meta.fields
            if isinstance(field, ForeignKey)]
        for field in model._meta.fields:
            if isinstance(field, ForeignKey):
                if field.related_model not in models:
                    yield field.name
                    yield from [
                        f"{field.name}__{fn}" for fn in self.orderable_fields(
                            field.related_model, new_models)]
                continue
            else:
                yield field.name == 'id' and 'pk' or field.name

    def object_meta_list(self):
        """Build metadata for the view model list.

        :returns: The metadata
        :rtype: :class:`dict`
        """
        default_all = not self.request.GET.keys()
        meta = {}
        if get_bool(self.request.GET, 'fields', default_all):
            meta['fields'] = cache.get_or_set(
                class_key(self.__class__, 'meta', 'list_fields'),
                lambda: {
                    n: f.meta() for n, f in self.get_list_fields().items()},
                None)
        if get_bool(self.request.GET, 'filters', default_all):
            meta['filters'] = cache.get_or_set(
                class_key(self.__class__, 'meta', 'filters'),
                lambda: [_f.meta for _f in self.filters],
                None)
        if get_bool(self.request.GET, 'orders', default_all):
            meta['orders'] = cache.get_or_set(
                class_key(self.__class__, 'meta', 'orders'),
                lambda: list(self.orderable_fields(self.model)),
                None)
        return meta

    @rest_api("/meta/list", method="get", parameters=[
        parameters.groups.MetaList], response_schema='meta_list_schema',
        priority_doc=10)
    def get_meta_list(self, *args, **kwargs):
        """Entrypoint for :code:`GET /meta/list` route.

        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        get:
            summary: Get {models} list metadata
        """
        return JsonResponse(self.object_meta_list())

    def apply_view_filter(self, qs):
        """Apply view filters on queryset.

        :param qs: The source queryset
        :type qs: :class:`django.db.models.QuerySet`
        :returns: The filtered queryset
        :rtype: :class:`django.db.models.QuerySet`
        """
        for filter in self.filters:
            qs = qs.filter(filter.query(self.request.GET))
        return qs

    def apply_view_search(self, qs):
        """Apply view search on queryset.

        :param qs: The source queryset
        :type qs: :class:`django.db.models.QuerySet`
        :returns: The filtered queryset
        :rtype: :class:`django.db.models.QuerySet`
        """
        search = self.request.GET.get('search')
        if search:
            return qs.filter(self.search_filter(search))
        return qs

    def get_order_mapping(self):
        return {}

    def get_query_order(self):
        omap = self.get_order_mapping()

        def apply(o):
            if not o:
                return o
            if o[0] == '+':
                o = o[1:]
            s, fn = o[0] in '-' and ('-', o[1:]) or ('', o)
            return f"{s}{omap.get(fn, fn)}"

        order = self.request.GET.get('order')
        return order and [apply(o) for o in order.split(',')] or order

    def apply_view_order(self, qs):
        """Apply view order on queryset.

        :param qs: The source queryset
        :type qs: :class:`django.db.models.QuerySet`
        :returns: The ordered queryset
        :rtype: :class:`django.db.models.QuerySet`
        """
        order = self.get_query_order()
        if order:
            try:
                return qs.order_by(*order)
            except FieldError as e:
                raise APIError(e.args[0])
        return qs.order_by(*self.model._meta.ordering)

    def get_list_queryset(self, select_related=None, prefetch_related=None):
        """Get list queryset.

        The result queryset is filtered and ordered by view settings.

        :param select_related: Arguments for queryset select_related
        :type select_related: :class:`list[str]`
        :param prefetch_related: Arguments for queryset prefetch_related
        :type prefetch_related: :class:`list[str]`
        :returns: The filtered queryset
        :rtype: :class:`django.db.models.QuerySet`
        """
        qs = super().get_list_queryset(select_related, prefetch_related)
        qs = self.apply_view_filter(qs)
        qs = self.apply_view_search(qs)
        qs = self.apply_view_order(qs)
        return qs.distinct()

    def get_list_fields_select_related(self):
        """:meta private: Undocumented because it must be changed."""
        return cache.get_or_set(
            class_key(self.__class__, 'list_fields', 'select_related'),
            lambda: set([
                _f for field in self.get_list_fields().values()
                for _f in field.select_related]),
            None)

    def get_list_fields_prefetch_related(self):
        """:meta private: Undocumented because it must be changed."""
        return cache.get_or_set(
            class_key(self.__class__, 'list_fields', 'prefetch_related'),
            lambda: set([
                _f for field in self.get_list_fields().values()
                for _f in field.prefetch_related]),
            None)

    def get_list_result(self, qs):
        """Get a generator to serialize each result in a queryset.

        :param qs: The source queryset
        :type qs: :class:`django.db.models.QuerySet`
        :returns: The generator
        :rtype: :class:`generator`
        """
        qs = qs.select_related(
            *self.get_list_fields_select_related()
        ).prefetch_related(
            *self.get_list_fields_prefetch_related())
        for o in qs:
            yield self.serialize_object(o, **{
                _f.alias: _f.to_json(o, self.format_date)
                for _f in self.get_list_fields().values()})

    def get_short_list_result(self, qs):
        """Get a generator to serialize each result in a queryset.

        Each result is serialized with its simple representation (json_repr
        od default representation).

        :param qs: The source queryset
        :type qs: :class:`django.db.models.QuerySet`
        :returns: The generator
        :rtype: :class:`generator`
        """
        for o in qs:
            if isinstance(o, JSONReprMixin):
                yield o.json_repr()
            else:
                yield dict(
                    pk=o.pk,
                    resource_name=str(o))

    def pagination_result(self, qs):
        """Apply pagination on a queryset.

        :param qs: The source queryset
        :type qs: :class:`django.db.models.QuerySet`
        :returns: The queryset for the active page and the pagination data
        :rtype: :class:`tuple(django.db.models.QuerySet, dict)`
        """
        page_size = get_int(self.request.GET, 'page_size', 10)
        if settings.PFX_MAX_LIST_RESULT_SIZE:
            page_size = min(page_size, settings.PFX_MAX_LIST_RESULT_SIZE)
        page = get_int(self.request.GET, 'page', 1)
        page_subset = get_int(self.request.GET, 'page_subset', 5)
        count = qs.count()
        page_count = (1 + (count - 1) // page_size) or 1
        offset = (page - 1) * page_size
        subset_first = min(
            max(page - page_subset // 2, 1),
            max(page_count - page_subset + 1, 1))
        qs = qs.all()[offset:offset + page_size]
        return qs, dict(
            page_size=page_size,
            page=page,
            page_subset=page_subset,
            count=count,
            page_count=page_count,
            subset=list(range(
                subset_first,
                min(subset_first + page_subset, page_count + 1))))

    def offset_result(self, qs):
        """Apply offset/limit on a queryset.

        :param qs: The source queryset
        :type qs: :class:`django.db.models.QuerySet`
        :returns: The queryset for the active page and the pagination data
        :rtype: :class:`tuple(django.db.models.QuerySet, dict)`
        """
        limit = get_int(self.request.GET, 'limit', 10)
        if settings.PFX_MAX_LIST_RESULT_SIZE:
            limit = min(limit, settings.PFX_MAX_LIST_RESULT_SIZE)
        offset = get_int(self.request.GET, 'offset', 0)
        count = qs.count()
        page_count = (1 + (count - 1) // limit) or 1
        qs = qs[offset:offset + limit]
        return qs, dict(
            count=count,
            page_count=page_count,
            limit=limit,
            offset=offset)

    def _get_list_extra_meta(self):
        return {}

    def _get_list(self, *args, **kwargs):
        res = {}
        meta = {}
        qs = self.get_list_queryset()
        subset = self.request.GET.get('subset', self.Subset.NONE)
        if get_bool(self.request.GET, 'count'):
            meta['count'] = qs.count()
        if subset == self.Subset.PAGINATION:
            qs, meta['subset'] = self.pagination_result(qs)
        elif subset == self.Subset.OFFSET:
            qs, meta['subset'] = self.offset_result(qs)
        elif settings.PFX_MAX_LIST_RESULT_SIZE:
            qs = qs[:settings.PFX_MAX_LIST_RESULT_SIZE]
        meta.update(self._get_list_extra_meta())
        if meta:
            res['meta'] = meta
        if get_bool(self.request.GET, 'items', 'count' not in meta):
            if self.request.GET.get('mode', 'list') == 'select':
                res['items'] = list(self.get_short_list_result(qs))
            else:
                res['items'] = list(self.get_list_result(qs))
        return JsonResponse(res)

    @rest_api(
        "", method="get", parameters=[parameters.groups.List],
        filters=True, search=True,
        response_schema='model_list_schema', priority_doc=-20)
    def get_list(self, *args, **kwargs):
        """Entrypoint for :code:`GET /` route.

        Retrieve an object list response.

        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        get:
            summary: Get {models} list
        """

        return self._get_list(*args, **kwargs)

    @classmethod
    def generate_schemas(cls):
        """Generate schemas for the class.
        """
        from .fields import FieldType
        super().generate_schemas()
        cls.meta_list_schema = Schema('list_meta', "Meta", properties=dict(
            fields=dict(
                type='array', items=dict(type='object', properties=dict(
                    name=dict(type='string'),
                    type=dict(
                        type='string',
                        enum=list(FieldType.APIDOC_FIELD_BINDING.keys())),
                    choices=dict(
                        type='array', items=dict(type='string'),
                        example=["value1", "value2"]),
                    readonly=dict(type='object', properties=dict(
                        post=dict(type='boolean'),
                        put=dict(type='boolean'))),
                    required=dict(type='boolean'))),
                description="List of fields."),
            filters=dict(
                type='array', items=dict(type='object', properties=dict(
                    name=dict(type='string'),
                    label=dict(type='string'),
                    type=dict(
                        type='string',
                        enum=list(FieldType.APIDOC_FIELD_BINDING.keys())),
                    choices=dict(
                        type='array', items=dict(type='string'),
                        example=["value1", "value2"]),
                    empty_value=dict(type='boolean'),
                    technical=dict(type='boolean'),
                    related_model=dict(type='string'))),
                description="List of fields."),
            orders=dict(
                type='array', items=dict(type='string'),
                description="List of orderable fields.",
                example=['field1', 'field2', 'field3'])))
        cls.model_list_schema = ModelListSchema(
            cls.model, cls._process_fields(cls.list_fields or cls.fields))

    @classmethod
    def get_apidoc_schemas(cls):
        """Get schemas for the class.

        :returns: The schemas list
        :rtype: :class:`list[pfx.pfxcore.apidoc.Schema]`
        """
        return super().get_apidoc_schemas() + [
            cls.meta_list_schema, cls.model_list_schema]


class DetailRestViewMixin(ModelResponseMixin):
    """Extension mixin to add a get detail route."""

    @rest_api("/<int:id>", method="get", parameters=[
        parameters.groups.ModelSerialization], response_schema='model_schema',
        priority_doc=-10)
    def get(self, id, *args, **kwargs):
        """Entrypoint for :code:`GET /<int:id>` route.

        Retrieve an object detail by ID.

        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        get:
            summary: Get {model}
            parameters extras:
                id: the {model} pk
        """
        obj = self.get_object(pk=id)
        return self.response(obj)


class SlugDetailRestViewMixin(ModelResponseMixin):
    """Extension mixin to add a get detail by slug route."""

    #: The slug field name
    SLUG_FIELD = "slug"

    @rest_api(
        "/slug/<slug:slug>", method="get",
        parameters=[parameters.groups.ModelSerialization],
        response_schema='model_schema', priority_doc=-10)
    def get_by_slug(self, slug, *args, **kwargs):
        """Entrypoint for :code:`GET /slug/<slug:slug>` route.

        Retrieve an object detail by slug.

        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        get:
            summary: Get {model} by slug
            parameters extras:
                slug: the {model} slug name
        """
        obj = self.get_object(**{self.SLUG_FIELD: slug})
        return self.response(obj)


class CreateRestViewMixin(ModelBodyMixin, ModelResponseMixin):
    """Extension mixin to add create route."""

    #: Default values
    default_values = {}

    def get_default_values(self):
        """Get default values

        :returns: The default values
        :rtype: :class:`dict`
        """
        return dict(self.default_values)

    def new_object(self):
        """Get a new object instance with default values.

        :returns: A model instance
        :rtype: :class:`django.db.models.Model`
        """
        return self.model(**self.get_default_values())

    def object_create_perm(self, data):
        """Return :code:`True` if an instance can be created.

        This method returns always :code:`True`. It is designed to be
        overloaded to customize permissions. You can customize depending
        on user and/or creation data.

        :param data: The data used to create instance
        :returns: A model instance
        :rtype: :class:`django.db.models.Model`
        """
        return True

    def _post(self, *args, **kwargs):
        obj = self.new_object()
        data, rel_data = self.get_model_data(
            obj, self.deserialize_body(), created=True)
        forbidden = False
        if not self.object_create_perm(data):
            forbidden = True
        self.set_values(obj, **data)
        try:
            self.validate(obj, created=True)
            if forbidden:
                raise ForbiddenError
            return self.is_valid(obj, created=True, rel_data=rel_data)
        except ValidationError as e:
            return self.is_invalid(obj, errors=e)

    @rest_api(
        "", method="post", parameters=[parameters.groups.ModelSerialization],
        request_schema='model_create_schema',
        response_schema='model_message_schema', priority_doc=-20)
    def post(self, *args, **kwargs):
        """Entrypoint for :code:`POST /` route.

        Create an object from JSON body.

        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        post:
            summary: Create {model}
        """
        return self._post(*args, **kwargs)


class UpdateRestViewMixin(ModelBodyMixin, ModelResponseMixin):
    """Extension mixin to add create route."""

    def object_update_perm(self, obj, data):
        """Return :code:`True` if an instance can be updated.

        This method returns always :code:`True`. It is designed to be
        overloaded to customize permissions. You can customize depending
        on user, current instance and/or updated data.

        :param obj: Current instance
        :param data: The data used to create instance
        :returns: A model instance
        :rtype: :class:`django.db.models.Model`
        """
        return True

    def _put(self, id, *args, **kwargs):
        obj = self.get_object(pk=id)
        data, rel_data = self.get_model_data(
            obj, self.deserialize_body(), created=False)
        forbidden = False
        if not self.object_update_perm(obj, data):
            forbidden = True
        self.set_values(obj, **data)
        try:
            self.validate(obj, created=False)
            if forbidden:
                raise ForbiddenError
            return self.is_valid(obj, created=False, rel_data=rel_data)
        except ValidationError as e:
            return self.is_invalid(obj, errors=e)

    @rest_api(
        "/<int:id>", method="put",
        parameters=[parameters.groups.ModelSerialization],
        request_schema='model_update_schema',
        response_schema='model_message_schema',
        priority_doc=-10)
    def put(self, id, *args, **kwargs):
        """Entrypoint for :code:`PUT /<int:id>` route.

        Update an object from JSON body.

        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        put:
            summary: Update {model}
            parameters extras:
                id: the {model} pk
        """
        return self._put(id, *args, **kwargs)


class DeleteRestViewMixin(ModelMixin):
    """Extension mixin to add delete route."""

    def object_delete_perm(self, obj):
        """Return :code:`True` if an instance can be updated.

        This method returns always :code:`True`. It is designed to be
        overloaded to customize permissions. You can customize depending
        on user and/or current instance.

        :param obj: Current instance
        :returns: A model instance
        :rtype: :class:`django.db.models.Model`
        """
        return True

    def _delete(self, id, *args, **kwargs):
        obj = self.get_object(pk=id)
        if not self.object_delete_perm(obj):
            raise ForbiddenError()
        self.delete_object(obj)
        return self.message_response(f(
            _("{model} {obj} deleted."), model=self.model_name, obj=obj))

    @rest_api(
        "/<int:id>", method="delete", response_schema='message_schema',
        priority_doc=-10)
    def delete(self, id, *args, **kwargs):
        """Entrypoint for :code:`DELETE /<int:id>` route.

        Delete an object from JSON body.

        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        delete:
            summary: Delete {model}
            parameters extras:
                id: the {model} pk
        """
        return self._delete(id, *args, **kwargs)


class MediaRestViewMixin(ModelMixin):
    """Extension mixin to manage media fields."""

    def _get_model_field(self, field):
        try:
            model_field = self.model._meta.get_field(field)
            if not isinstance(model_field, MediaField):
                raise NotFoundError  # pragma: no cover
        except FieldDoesNotExist:  # pragma: no cover
            raise NotFoundError
        return model_field

    @rest_api(
        "/<int:pk>/<str:field>/upload-url/<str:filename>", method="get",
        priority_doc=-8)
    def field_media_upload_url(self, pk, field, filename, *args, **kwargs):
        """Entrypoint for
        :code:`GET /<int:pk>/<str:field>/upload-url/<str:filename>` route.

        Get the upload URL for a media file.

        :param pk: The object pk
        :param field: The field name
        :param filename: The file name
        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        get:
            summary: Get upload URL
            description: |
                Get upload URL for a `MediaField` field.

                You can upload a file ont the received URL. When the upload
                query is done, you have to confirm the process with an
                update request (`PUT`) on {model}. The body of this request
                must contain the name of the `MediaField` with the contents
                of the `file` value in the response of this request.

                1. `GET /<int:pk>/<str:field>/upload-url/<str:filename>`
                    → `data`
                2. `PUT data.url aFile Content-Type: aFile.type`
                3. `PUT /<int:pk> {{field: data.file}}`
            parameters extras:
                pk: The {model} pk.
                field: The {model} field name. Must be the name of
                    a `MediaField` field.
                filename: The desired filename.
            responses:
                200:
                    description: The upload URL
                    content:
                        application/json:
                            schema:
                                properties:
                                    url:
                                        type: string
                                        format: uri
                                    file:
                                        type: object
                                        properties:
                                            name:
                                                type: string
                                            key:
                                                type: string
        """
        obj = self.get_object(pk=pk)
        try:
            res = self._get_model_field(field).get_upload_url(
                self.request, obj, filename)
        except StorageException as e:  # pragma: no cover
            logger.exception(e)
            raise APIError(_("Unexpected storage error", status=500))
        return JsonResponse(res)

    @rest_api(
        "/<int:pk>/<str:field>", method="get",
        parameters=[parameters.MediaRedirect], priority_doc=-9)
    def field_media_get(self, pk, field, *args, **kwargs):
        """Entrypoint for :code:`GET /<int:pk>/<str:field>` route.

        Get the download URL for a media file.

        :param pk: The object pk
        :param field: The field name
        :returns: The JSON response
        :rtype: :class:`JsonResponse`
        ---
        get:
            summary: Get {model} file
            description: Get the URL for a media field file.
            parameters extras:
                pk: the {model} pk
                field: the {model} field name
            responses:
                200:
                    description: The file URL, if `redirect` is `false`.
                    content:
                        application/json:
                            schema:
                                properties:
                                    url:
                                        type: string
                                        format: uri
                302:
                    description: The redirect, if `redirect` is `true`.
        """
        obj = self.get_object(pk=pk)
        try:
            url = self._get_model_field(field).get_url(self.request, obj)
        except StorageException as e:  # pragma: no cover
            logger.exception(e)
            raise APIError(_("Unexpected storage error", status=500))
        if get_bool(self.request.GET, 'redirect'):
            return redirect(url)
        return JsonResponse(dict(url=url))


class SecuredRestViewMixin(View):
    """A view mixin to manage service permissions.

    You can add :code:`${func_name}_public` class attributes to override
    :code:`default_public` value for specifics methods. This attribute has
    precedence over the :code:`public` attribute of the :code:`@rest_api`
    decorator, then you can override the behavior in an inherited view
    without overriding the entrypoint method.

    You can add :code:`${func_name}_perm` method to customize permissions
    checks for a dedicated service.
    """

    #: If :code:`True` the services are public by default.
    default_public = False

    def perm(self):
        """Check default permissions for all services.

        Can be overloaded to customize behavior.

        If this method returns :code:`False`, the access is always denied.
        Otherwise custom checks of the service are performed.
        """
        return True

    def _is_public(self, public, func_name):
        param = f'{func_name}_public'
        if hasattr(self, param):
            return getattr(self, param)
        return self.default_public if public is None else public

    def check_perm(self, public, func_name, *args, **kwargs):
        """Check permissions for a specific service.

        Do all checks for a specific service and raise
        :class:`UnauthorizedError` or :class:`ForbiddenError` if needed.

        :param public: The object pk
        :param field: The field name
        """
        if self._is_public(public, func_name):
            return
        if not self.request.user.is_authenticated:
            raise UnauthorizedError()
        if not self.perm():
            raise ForbiddenError()
        fperm = f'{func_name}_perm'
        if hasattr(self, fperm) and not getattr(self, fperm)(*args, **kwargs):
            raise ForbiddenError()


class BaseRestView(SecuredRestViewMixin, View):
    """The base class for REST views."""

    #: :meta private: Internal for as_view binding.
    pfx_methods = None
    #: :meta private: Internal for as_view binding.
    rest_view_path = {}
    #: :meta private: Internal for as_view binding.
    rest_doc = {}
    #: :meta private: Internal for as_view binding.
    rest_doc_priority = {}
    #: Tags for ApiDoc.
    tags = None
    #: Schemas for ApiDoc.
    schemas = []
    #: Message schema for ApiDoc.
    message_schema = None

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, self.pfx_methods.get(
                    request.method.lower(), 'http_method_not_allowed'),
                self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    @staticmethod
    def _path_order(path, methods):
        def process(e):
            e = re.sub(r'<path:.*>', '!01', e)
            e = re.sub(r'<int:.*>', '!03', e)
            e = re.sub(r'<uuid:.*>', '!04', e)
            e = re.sub(r'<slug:.*>', '!05', e)
            e = re.sub(r'<str:.*>', '!06', e)
            e = re.sub(r'<.*>', '!02', e)
            return e

        return methods.get('priority', 0), *map(
            process, path.lstrip('/').split('/'))

    @staticmethod
    def _path_order_doc(path, methods):
        return methods.get('priority_doc', 0), path.lstrip('/').split('/')

    @classmethod
    def get_urls(cls, as_pattern=False):
        """Generate URLs for the view."""
        def fullpath(p2):
            res = f'{cls.rest_view_path[cls]}{p2}'.lstrip('/')
            return res if as_pattern else f'/{res}'

        paths = {}
        for name in dir(cls):
            m = getattr(cls, name, None)
            if m and callable(m) and hasattr(m, 'rest_api_method'):
                methods = paths.setdefault(m.rest_api_path, dict(
                    priority=0, priority_doc=0))
                methods[m.rest_api_method] = name
                if m.rest_api_priority != 0:
                    if methods['priority'] not in (0, m.rest_api_priority):
                        raise Exception(
                            f"Path {fullpath(m.rest_api_path)}: "
                            "you cannot set different priority for same path")
                    methods['priority'] = m.rest_api_priority

                priority_doc = cls.rest_doc_priority.get(
                    (fullpath(m.rest_api_path), m.rest_api_method),
                    m.rest_api_priority_doc)
                if priority_doc != 0:
                    if methods['priority_doc'] not in (
                            0, m.rest_api_priority_doc):
                        raise Exception(
                            f"Path {fullpath(m.rest_api_path)}: "
                            "you cannot set different priority_doc "
                            "for same path")
                    methods['priority_doc'] = m.rest_api_priority_doc
        return [
            path(fullpath(p), cls.as_view(pfx_methods=ms)) if as_pattern
            else dict(path=fullpath(p), methods={
                k: v for k, v in ms.items()
                if k not in ('priority', 'priority_doc')})
            for p, ms in sorted(
                paths.items(), key=lambda e:
                    cls._path_order(*e) if as_pattern
                    else cls._path_order_doc(*e),
                reverse=as_pattern)]

    @classmethod
    def as_urlpatterns(cls):
        """Get URLs patterns for the view."""
        if cls not in __PFX_VIEWS__:
            __PFX_VIEWS__.append(cls)
        return cls.get_urls(as_pattern=True)

    @classmethod
    def get_apidoc_tags(cls):
        """Get ApiDoc tags."""
        return cls.tags or [Tag(str(cls.__name__))]

    @classmethod
    def generate_schemas(cls):
        """Generate schemas for the class.
        """
        cls.message_schema = Schema('Message', "Message", properties=dict(
            message=dict(type='string')))

    @classmethod
    def get_apidoc_schemas(cls):
        """Get schemas for the class.

        :returns: The schemas list
        :rtype: :class:`list[pfx.pfxcore.apidoc.Schema]`
        """
        return cls.schemas + [cls.message_schema]


class RestView(
        ListRestViewMixin,
        DetailRestViewMixin,
        CreateRestViewMixin,
        UpdateRestViewMixin,
        DeleteRestViewMixin,
        BaseRestView):
    pass
