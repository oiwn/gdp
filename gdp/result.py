# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import cerberus
import collections


def _make_types(schema):
    """Make values allowed by schame accessable as a class attributes
    >>> s = {'a': {'allowed': ['yes', 'no'], 'required': True}}
    >>> c = _make_types(s)
    >>> c.a.YES == 'yes'
    >>> True

    Or with result class

    >>> r = SomeResult(dict(success=True, op='updated', step='save'))
    >>> r.types.op.UPDATED == r.op
    >>> True
    """
    if not isinstance(schema, dict):
        raise AttributeError('`schema` should be an instance of dict')

    cls_dict = {}
    for s_key, s_val in schema.items():
        if s_val['required'] is True and 'allowed' in s_val:
            allowed = {str(x).upper(): x for x in s_val['allowed']}
            cls_dict[s_key] = type(s_key, (object, ), allowed)
    return type('ResultTypes', (object, ), cls_dict)


class AbstractResult(collections.abc.Mapping):
    """Container type for pipeline step result.

    >>> class MongoResult(AbstractResult):
    >>>     schema = {
    >>>         '_id': {'type': 'string'},
    >>>         'code': {
    >>>             'type': 'number', 'required': True, 'allowed': ['ok', 'err']
    >>>         }
    >>>     }

    >>> result = MongoResult(dict(_id='longhashnumber', code='ok'))
    >>> assert result.code == 'ok'
    >>> assert MongoResult.types.code.OK == result.code

    :param document: result parameters (should fit defined schema)
    :type document: dict
    :return: instance of `AbstractResult` subclass
    :rtype: `AbstractResult`
    """

    schema = None
    types = None
    _mapping = None

    _validator = cerberus.Validator()

    def __new__(cls, document, **kwargs):
        cls._validator = cerberus.Validator(cls.schema)
        cls.types = _make_types(cls.schema)
        return super().__new__(cls, **kwargs)

    def __init__(self, document, *args, **kwargs):
        if not self._validator.validate(document):
            raise cerberus.DocumentError(
                'Wrong args: {}'.format(self._validator.errors))
        self._mapping = document

    def __getattr__(self, key):
        if key in self._mapping:
            return self._mapping[key]
        else:
            raise AttributeError("No attribute \"{}\" in {}".format(
                key, list(self._mapping.keys())))

    def __getitem__(self, key):
        return self._mapping[key]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping.keys())

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self._mapping)

    def as_dict(self):
        return dict(self._mapping)
