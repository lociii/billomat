# -*- coding: UTF-8 -*-
import copy
import json
import requests
import six
import time
from uuid import uuid4


class BillomatException(Exception):
    pass


class BillomatRequestException(BillomatException):
    pass


class BilllomatInvalidFilterException(BillomatException):
    pass


class BillomatMultipleObjectsReturned(BillomatException):
    pass


class BillomatValidationException(BillomatException):
    pass


class BillomatReadOnlyException(BillomatException):
    pass


# define django signals
billomatclient_request = None
billomatclient_response = None
billomatclient_error = None
try:
    import django.dispatch
    billomatclient_request = django.dispatch.Signal(providing_args=['method', 'url', 'headers', 'params', 'data',
                                                                    'request_id'])
    billomatclient_response = django.dispatch.Signal(providing_args=['method', 'url', 'headers', 'params', 'data',
                                                                     'response', 'request_id'])
    billomatclient_error = django.dispatch.Signal(providing_args=['method', 'url', 'headers', 'params', 'data',
                                                                  'exception', 'request_id'])
except ImportError:
    pass


class Client(object):
    METHOD_GET = 'GET'
    METHOD_POST = 'POST'
    METHOD_PUT = 'PUT'
    METHOD_DELETE = 'DELETE'
    MAX_LIMIT = 1000

    api_name = None
    api_key = None
    app_id = None
    app_secret = None
    sleep = 0

    _URL = 'https://%(api_name)s.billomat.net/api/%(resource)s'

    def query(self, resource, params=None, data=None, method=METHOD_GET):
        request_id = uuid4()
        params = params or {}
        data = data or {}

        url = self._URL % {
            'api_name': self.api_name,
            'resource': resource,
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BillomatApiKey': self.api_key,
        }

        if self.app_id and self.app_secret:
            headers['X-AppId'] = self.app_id
            headers['X-AppSecret'] = self.app_secret

        if billomatclient_request:
            billomatclient_request.send(sender=self.__class__, method=method, url=url, headers=headers, params=params,
                                        data=data, request_id=request_id)

        try:
            request = requests.Request(method=method, url=url, headers=headers, params=params, data=json.dumps(data))
            r = request.prepare()

            s = requests.Session()
            response = s.send(r)

            # optional sleep to avoid rate limit exceedance - use settings.BILLOMAT_CLIENT_SLEEP
            time.sleep(self.sleep)
        except Exception as e:
            if billomatclient_error:
                billomatclient_error.send(sender=self.__class__, method=method, url=url, headers=headers, params=params,
                                          data=data, exception=e, request_id=request_id)

            raise BillomatRequestException('request failed: %s' % str(e))

        if billomatclient_response:
            billomatclient_response.send(sender=self.__class__, method=method, url=url, headers=headers, params=params,
                                         data=data, response=response, request_id=request_id)

        if response.text == '':
            return {}

        try:
            result = response.json()

            if result is None:
                raise BillomatRequestException('null response')

            if 'errors' in result:
                raise BillomatRequestException(result['errors']['error'])

            return result
        except ValueError:
            raise BillomatRequestException('malformed response: "%s"' % response.text)


class QuerySet(object):
    def __init__(self, object_manager):
        self.object_manager = object_manager
        self._iterator = QuerySetIterator(queryset=self)
        self.params = {}

    def __len__(self):
        cnt = self._iterator.get_total()
        if cnt is None:
            self._iterator.get_page()
            cnt = self._iterator.get_total()
            self._iterator.reset()

        return cnt

    def filter(self, **kwargs):
        self.object_manager.validate_kwargs(kwargs)

        cloned_qs = copy.deepcopy(self)
        cloned_qs.params.update(kwargs)
        return cloned_qs

    def count(self):
        return len(self)

    def __iter__(self):
        return self._iterator

    def __unicode__(self):
        return u'<QuerySet of "%s">' % self.object_manager.resource


class QuerySetIterator(object):
    def __init__(self, queryset):
        assert isinstance(queryset, QuerySet)

        self.queryset = queryset
        self.total = None
        self._result_cache = []
        self._page = 0
        self._position = 0

    def __iter__(self):
        return self

    def reset(self):
        self.total = None
        self._result_cache = []
        self._page = 0
        self._position = 0

    def next(self):
        if (
            self.total is None
            or
            len(self._result_cache) <= self._position < self.total
        ):
            self.get_page()

        # return item from cache
        try:
            model = self.queryset.object_manager.get_instance(
                data=self._result_cache[self._position]
            )
            self._position += 1
            return model
        except IndexError:
            pass

        # no more items
        self._position = 0
        raise StopIteration

    def get_page(self):
        resource = self.queryset.object_manager.resource
        object_name = self.queryset.object_manager.object_name
        if self._page is None:
            self._page = 0
        self._page += 1

        params = self.queryset.params
        params.update({
            'per_page': self.queryset.object_manager.client.MAX_LIMIT,
            'page': self._page,
        })

        result = self.queryset.object_manager.client.query(
            resource=resource,
            params=params,
        )

        # handle single object response
        objects = []
        if resource in result and object_name in result[resource]:
            objects = result[resource][object_name]
            if isinstance(objects, dict):
                objects = [objects, ]
            self.total = int(result[resource]['@total'])
            self._page = int(result[resource]['@page'])
        elif object_name in result:
            objects = [result[object_name], ]
            self.total = 1

        self._result_cache += objects

    def get_total(self):
        return self.total


class ObjectManager(object):
    client = Client()

    def __init__(self, resource, filters, object_name, model):
        self.resource = resource
        self.object_name = object_name
        self._filters = filters
        self._model = model

    def get_instance(self, data):
        return self._model(**data)

    def _get_queryset(self):
        return QuerySet(object_manager=self)

    def validate_kwargs(self, kwargs):
        for key, value in kwargs.items():
            if key not in self._filters:
                raise BilllomatInvalidFilterException(
                    'filter %s not valid for resource %s' % (
                        key,
                        self.resource
                    )
                )

    def create(self, *args, **kwargs):
        model = self._model(**kwargs)
        model.save()
        return model

    def all(self):
        return self._get_queryset()

    def get(self, *args, **kwargs):
        self.validate_kwargs(kwargs)
        qs = self._get_queryset().filter(**kwargs)
        if len(qs) > 1:
            raise BillomatMultipleObjectsReturned()

        return next(iter(qs))

    def filter(self, *args, **kwargs):
        self.validate_kwargs(kwargs)
        return self._get_queryset().filter(**kwargs)


class ModelBase(type):
    def __new__(mcs, name, bases, attrs):
        super_new = super(ModelBase, mcs).__new__

        # attrs will never be empty for classes declared in the standard way
        # (ie. with the `class` keyword). This is quite robust.
        if name == 'NewBase' and attrs == {}:
            return super_new(mcs, name, bases, attrs)

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, ModelBase) and
                   not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))]
        if not parents:
            return super_new(mcs, name, bases, attrs)

        module = attrs.pop('__module__')
        new_class = super_new(mcs, name, bases, {'__module__': module})
        meta = attrs.pop('Meta', None)

        new_class.add_to_class('objects', ObjectManager(
            resource=meta.resource,
            filters=meta.filters,
            object_name=meta.object_name,
            model=new_class,
        ))

        # add anything else
        fields = {}
        for name, value in attrs.items():
            if isinstance(value, Field):
                fields[name] = value
            else:
                new_class.add_to_class(name, value)
        new_class.add_to_class('_fields', fields)

        return new_class

    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class Model(six.with_metaclass(ModelBase)):
    objects = None
    _fields = {}

    class Meta:
        resource = None
        object_name = None
        filters = ()

    def __init__(self, **kwargs):
        self.additional_data = {}

        # initialize fields
        self.fields = copy.deepcopy(self._fields)
        for name in self.fields:
            field = self.fields[name]
            if not field.name:
                field.name = name

        # set data
        for name, value in kwargs.items():
            if name in self.fields:
                self.fields[name].init_value(value)
            else:
                self.additional_data[name] = value

    def __setattr__(self, name, value):
        if hasattr(self, 'fields') and name in self.fields:
            self.fields[name].set_value(value)
        else:
            super(Model, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.fields:
            return self.fields[name]
        return getattr(self, name)

    def __delattr__(self, name):
        if name in self.fields:
            raise BillomatException('cannot remove field from model')
        return super(Model, self).__delattr__(self, name)

    def __unicode__(self):
        return u'<Billomat %s object %s>' % (
            self.__class__.__name__,
            self.id,
        )

    def dump(self):
        message = []
        for field in self.fields.values():
            message.append('%s (%s): %s' % (
                field.name,
                field.__class__.__name__,
                field.value,
            ))
        message = sorted(message)
        return "\n".join(message)

    def save(self, *args, **kwargs):
        # prepare data
        dirty = {}
        data = {}
        dataset_id = None
        response = None

        for field in self.fields.values():
            if not field.read_only and field.value != field.EMPTY_VALUE:
                data[field.name] = field.to_json()
            if field.is_dirty:
                dirty[field.name] = field.to_json()
            if field.name == 'id':
                dataset_id = field.value

        # append additional data
        for key, value in self.additional_data.items():
            data[key] = value
        self.additional_data = {}

        # create dataset
        if dataset_id == Field.EMPTY_VALUE:
            response = self.objects.client.query(
                resource=self.objects.resource,
                data={
                    self.objects.object_name: data,
                },
                method=Client.METHOD_POST
            )
        # update existing dataset
        elif len(dirty) > 0:
            response = self.objects.client.query(
                resource='%s/%s' % (self.objects.resource, dataset_id),
                data={
                    self.objects.object_name: dirty,
                },
                method=Client.METHOD_PUT,
            )
            for field in self.fields.values():
                field.is_dirty = False

        if response:
            for name, value in response[self.objects.object_name].items():
                try:
                    self.fields[name].init_value(value)
                except KeyError:
                    # ignore additional fields from api
                    pass

    def delete(self, *args, **kwargs):
        dataset_id = self.fields['id'].value
        if dataset_id == Field.EMPTY_VALUE:
            raise BillomatException('cannot delete unsaved dataset')

        self.objects.client.query(
            resource='%s/%s' % (self.objects.resource, dataset_id),
            method=Client.METHOD_DELETE,
        )
        self.fields['id'].value = Field.EMPTY_VALUE


class Field(object):
    EMPTY_VALUE = ''

    def __init__(
        self, default=None, read_only=False,
        required=False, field_name=None
    ):
        self.name = field_name or None
        self.default = default or self.EMPTY_VALUE
        self.value = self.default
        self.read_only = read_only
        self.required = required
        self.is_dirty = False

    def init_value(self, value):
        self.value = self.to_python(value)

    def set_value(self, value):
        if self.read_only:
            raise BillomatReadOnlyException(
                'field is read only: %s' % self.name
            )

        value = self.to_python(value)
        if value != self.value:
            self.value = value
            self.is_dirty = True

    def to_python(self, value):
        raise NotImplemented()

    def to_json(self):
        return unicode(self)

    def __unicode__(self):
        return unicode(self.value)

    def __str__(self):
        return str(self.value)

    class Meta:
        abstract = True


try:
    from django.conf import settings
    Client.api_name = getattr(settings, 'BILLOMAT_API_NAME', None)
    Client.api_key = getattr(settings, 'BILLOMAT_API_KEY', None)
    Client.app_id = getattr(settings, 'BILLOMAT_APP_ID', None)
    Client.app_secret = getattr(settings, 'BILLOMAT_APP_SECRET', None)
    Client.sleep = getattr(settings, 'BILLOMAT_CLIENT_SLEEP', 0)
except ImportError:
    pass
