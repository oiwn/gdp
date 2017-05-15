# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import pytest
from gdp import AbstractStorage, AbstractPipeline, AbstractResult


class SomeResult(AbstractResult):
    schema = {
        'success': {'type': 'boolean', 'required': True},
        'step': {'type': 'string', 'required': True},
        '_id': {'type': 'string'},
    }


class SomePipeline(AbstractPipeline):
    steps = (
        ('pre_filter', None),
        ('transform', None),
        ('post_filter', None),
        ('validate', None),
        ('save', None)
    )

    @classmethod
    def pre_filter(cls, data):
        return SomeResult(dict(success=True, step='filter'))

    @classmethod
    def transform(cls, data):
        return SomeResult(dict(success=True, step='transform'))

    @classmethod
    def post_filter(cls, data):
        return SomeResult(dict(success=True, step='filter'))

    @classmethod
    def validate(cls, data):
        return SomeResult(dict(success=True, step='validate'))

    @classmethod
    def save(cls, data):
        return SomeResult(
            dict(success=True, step='save', _id='abcdef'))


class SomeStorage(AbstractStorage):
    def persist(self, data):
        pipeline = self.pipeline_class(data)

        for step, result in pipeline.process(data):
            print(step, result)

        return self.result_class(dict(
            success=True, step='save', _id='42'))


def test_storage():
    class ItemStorage(SomeStorage):
        schema = {'name': {'type': 'string', 'required': True}}
        pipeline_class = SomePipeline
        result_class = SomeResult

    storage = ItemStorage()
    result = storage.persist({'name': 'item1'})
    assert result.success is True
    assert isinstance(result.as_dict(), dict)


@pytest.mark.xfail
def test_steps_allowed():
    class ItemStorage(SomeStorage):
        schema = {'name': {'type': 'string', 'required': True}}

    storage = ItemStorage()
    storage.persist({'name': 'item2'})
