# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import pytest
from gdp.storage import AbstractStorage


class SomeStorage(AbstractStorage):
    def persist(self, data):
        return self.result_class(
            success=True, op_type='inserted', step='save', _id=42)


@pytest.mark.xfail
def test_storage():
    class ItemStorage(SomeStorage):
        schema = {'name': {'type': 'string', 'required': True}}

    storage = ItemStorage()
    result = storage.persist({'name': 'item1'})
    assert result.status == 'ok'
    assert isinstance(result.as_dict(), dict)


@pytest.mark.xfail
def test_steps_allowed():
    class ItemStorage(SomeStorage):
        schema = {'name': {'type': 'string', 'required': True}}

    storage = ItemStorage()
    # print(storage.result_cls.__dict__)
    storage.persist({'name': 'item2'})
