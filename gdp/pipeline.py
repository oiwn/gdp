# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import six
import operator
from abc import ABCMeta


@six.add_metaclass(ABCMeta)
class AbstractPipeline(object):
    _steps = (
        ('pre_filter', None),
        ('transform', None),
        ('post_filter', None),
        ('validate', None),
        ('save', None),
    )

    @classmethod
    def get_steps(cls):
        return (operator.itemgetter(0) for x in cls._steps)
