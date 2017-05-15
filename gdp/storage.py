# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import six
from abc import ABCMeta, abstractmethod
from .result import AbstractResult
from .pipeline import AbstractPipeline


@six.add_metaclass(ABCMeta)
class AbstractStorage(object):
    """Abstract data storage"""
    schema = None
    schema_allow_unknown = False

    pipeline_class = None
    result_class = None

    def __init__(self, schema_allow_unknown=None, **kwargs):
        self.schema_allow_unknown = schema_allow_unknown or False
        self.pipeline_class = kwargs.get('pipeline_class', self.pipeline_class)
        self.result_class = kwargs.get('result_class', self.result_class)

    @abstractmethod
    def persist(self, data):
        raise NotImplementedError
