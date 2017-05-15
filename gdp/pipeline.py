# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import six
import operator
from abc import ABCMeta, abstractmethod


def _func_wrapper(f):
    pass


@six.add_metaclass(ABCMeta)
class AbstractStep(object):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def __call__(self, data):
        raise NotImplementedError


@six.add_metaclass(ABCMeta)
class AbstractPipeline(object):
    """Abstract data pipeline"""
    steps = (
        ('pre_filter', None),
        ('transform', None),
        ('post_filter', None),
        ('validate', None),
        ('save', None),
    )

    def __init__(self, data, **kwargs):
        # if not self._check_steps(self.steps):
        #     raise TypeError('All pipeline functions should be callable')
        steps = []
        for name, func in self.steps:
            if func is None:
                cls_func = getattr(self, name, None)
                if cls_func and callable(cls_func):
                    steps.append((name, cls_func))
        self.steps = tuple(steps)

    def process(self, data):
        for step, func in self.steps:
            yield (step, func(data))

    @classmethod
    def get_step_names(cls):
        return (operator.itemgetter(0) for x in cls.steps)

    @staticmethod
    def _check_steps(steps):
        return all([callable(f) or isinstance(AbstractStep) for n, f in steps])
