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

        # if not self._check_types(self.pipeline_class, self.result_class):
        #     raise TypeError('Wrong type for pipeline or result class')

    @abstractmethod
    def persist(self, data):
        raise NotImplementedError

    @staticmethod
    def _check_types(pipeline_class, result_class):
        is_result_subclass = issubclass(result_class, AbstractResult)
        is_pipeline_subclass = issubclass(pipeline_class, AbstractPipeline)
        return is_pipeline_subclass and is_result_subclass
