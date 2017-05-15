# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from .result import AbstractResult
from .pipeline import AbstractPipeline
from .storage import AbstractStorage


class StorageFactory(object):
    """Storage configuration"""

    @classmethod
    def build_storage(cls,
                      storage_class,
                      pipeline_class,
                      result_class,
                      **kwargs):
        """Build new storage instance from passed classes"""
        assert issubclass(storage_class, AbstractStorage)
        assert issubclass(result_class, AbstractResult)
        assert issubclass(pipeline_class, AbstractPipeline)

        return storage_class(pipeline_class, result_class)
