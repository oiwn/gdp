# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import pytest
import cerberus
import itertools
from gdp.result import AbstractResult, _make_types


class SomeResult(AbstractResult):
    schema = {
        'success': {'type': 'boolean', 'required': True},
        'op': {'type': 'string', 'required': True,
               'allowed': ['inserted', 'updated', 'skipped', 'failed']},
        'step': {'type': 'string', 'required': True},
        '_id': {'type': 'number', 'required': False}
    }

    @property
    def fail(self):
        return not self._mapping['success']


def test_make_types_normal_schema():
    schema = {
        'a': {
            'type': 'string', 'allowed': ['yes', 'no'], 'required': True
        }
    }
    types_cls = _make_types(schema)

    for k, val in schema.items():
        attr_cls = types_cls.__dict__[k]
        for v in val['allowed']:
            assert attr_cls.__dict__[v.upper()] == v

    assert types_cls.a.YES == 'yes'


def test_make_types_empty_schema():
    test_cls, types_cls = type('TestType', (object, ), {}), _make_types({})
    assert set(test_cls.__dict__.keys()) == set(types_cls.__dict__.keys())


def test_init_result():
    result = SomeResult(dict(success=True, op='inserted', step='save'))
    assert issubclass(SomeResult, AbstractResult)
    assert isinstance(result, AbstractResult)
    assert SomeResult.types.op.INSERTED == result.op


def test_init_results():
    # generate all possible variants
    all_success_vars = [True, False]
    all_op_vars = SomeResult.schema['op']['allowed']
    all_step_vars = ['save', 'validate', 'transform']

    result1 = SomeResult(
        dict(success=True, op=SomeResult.types.op.INSERTED, step='save', _id=42))
    assert result1._id == 42

    variants = itertools.product(
        all_success_vars, all_op_vars, all_step_vars)
    for success, op, step in variants:
        result = SomeResult(dict(success=success, op=op, step=step))
        assert result.success is success
        assert result.fail is not success
        assert result.op == op
        assert result.step == step
        assert result1 != result
        with pytest.raises(AttributeError):
            result._id


def test_init_result_not_allowed_values():
    with pytest.raises(cerberus.DocumentError):
        SomeResult(dict(success=False, op='bugged', step='save'))

    with pytest.raises(cerberus.DocumentError):
        SomeResult(dict(success='wrong', op='ddd', step='save'))

    with pytest.raises(AttributeError):
        AbstractResult(dict(success='wrong', op='ddd', step='save'))


def test_init_result_skipped_values():
    with pytest.raises(cerberus.DocumentError):
        SomeResult(dict(success=False, op_type='failed'))

    with pytest.raises(cerberus.DocumentError):
        SomeResult({})


def test_init_result_additional_kwargs():
    result = SomeResult(dict(success=True, op='updated', step='save', _id=743))
    assert result._id == 743


def test_init_result_additional_wrong_kwargs():
    with pytest.raises(cerberus.DocumentError):
        SomeResult(dict(success=True, op='inserted', step='save', number=743))

# def test_result_magic_method_conains():
#     result = AbstractResult('ok', 'updated', 'save', _id=743)

#     assert 'status' in result and '_id' in result  # __contains__
#     assert 'foo' not in result  # __contains__


# def test_result_magic_method_len():
#     result = AbstractResult('ok', 'updated', 'save', _id=743)

#     assert len(result) == 4  # __len__


# def test_result_magic_method_getitem():
#     result = AbstractResult('ok', 'updated', 'save', _id=743)

#     assert result['op_type'] == 'updated'  # __getitem__
#     with pytest.raises(KeyError):
#         result['otype']


# def test_result_magic_method_getattr():
#     result = AbstractResult('ok', 'updated', 'save', _id=743)

#     assert result.op_type == 'updated'  # __getattr__
#     with pytest.raises(AttributeError):  # __getattr__
#         result.foo
#     assert getattr(result, 'foo', 1) == 1  # __getattr__


# def test_result_magic_method_setattr():
#     result = AbstractResult('ok', 'updated', 'save', _id=743)

#     with pytest.raises(TypeError):
#         result.op_type = 'wrong'


# def test_result_magic_method_setitem():
#     result = AbstractResult('ok', 'updated', 'save', _id=743)

#     with pytest.raises(TypeError):
#         result['op_type'] = 'wrong'
