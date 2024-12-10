#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
# -------------------------------------------------------------------------------


"""
This module contains various usefull utilities for *Hawat* application.
"""

__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

from collections.abc import Callable
import copy
import csv
import datetime
import functools
import json
import math
import os
from typing import Any, TypeVar, cast
import uuid


class URLParamsBuilder:
    """
    Small utility class for building URL parameter dictionaries for various view
    endpoints.

    .. note::

        This class is still proof of concept and work in progress.
    """
    def __init__(self, skeleton = None):
        self.rules = []
        self.kwrules = {}
        self.skeleton = skeleton or {}

    @staticmethod
    def _add_scalar(dst, key, val):
        if val is not None:
            dst[key] = val

    @staticmethod
    def _add_vector(dst, key, val):
        if val is not None:
            dst.setdefault(key, []).append(val)

    def add_rule(self, key, as_list = False, optional = False):
        """
        Add new rule to URL parameter builder.

        :param str key: Name of the rule key.
        :param bool as_list: Indication that the rule parameter is a list of multiple values.
        :param bool optional: Indication that the rule parameter is optional.
        """
        if as_list:
            rule = [key, self._add_vector, True, optional]
            self.rules.append(rule)
        else:
            rule = [key, self._add_scalar, False, optional]
            self.rules.append(rule)
        return self

    def add_kwrule(self, key, as_list = False, optional = False):
        """
        Add new keyword rule to URL parameter builder.

        :param str key: Name of the rule key.
        :param bool as_list: Indication that the rule parameter is a list of multiple values.
        :param bool optional: Indication that the rule parameter is optional.
        """
        if as_list:
            rule = [key, self._add_vector, True, optional]
            self.kwrules[key] = rule
        else:
            rule = [key, self._add_scalar, False, optional]
            self.kwrules[key] = rule
        return self

    def get_params(self, *args, **kwargs):
        """
        Get URL parameters as dictionary with filled-in values.
        """
        tmp = copy.deepcopy(self.skeleton)
        for idx, rule in enumerate(self.rules):
            try:
                rule[1](tmp, rule[0], args[idx])
            except IndexError:
                if not rule[3]:
                    raise
        for key, rule in self.kwrules.items():
            if key in kwargs:
                rule[1](tmp, rule[0], kwargs[key])
        return tmp


class LimitCounter:
    """
    Simple configurable limit counter with support for multiple keys.
    """
    def __init__(self, limit):
        self.counters = {}
        self.limit    = limit

    def count_and_check(self, key, increment = 1):
        """
        Increment key counter and check against internal limit.
        """
        self.counters[key] = self.counters.get(key, 0) + increment
        return self.counters[key] <= self.limit


#------------------------------------------------------------------------------


def get_timedelta(tstamp):
    """
    Get timedelta from current UTC time and given datetime object.

    :param datetime.datetime: Datetime of the lower timedelta boundary.
    :return: Timedelta object.
    :rtype: datetime.timedelta
    """
    return datetime.datetime.utcnow() - tstamp


def get_datetime_utc(aware = False):
    """
    Get current UTC datetime.

    :return: Curent UTC datetime.
    :rtype: datetime.datetime
    """
    if aware:
        return datetime.datetime.now(datetime.timezone.utc)
    return datetime.datetime.utcnow()


def parse_datetime(dtstring):
    """
    Parse given datetime string.

    :param str dtstring: Datetime string in ISON format to parse.
    :return: Curent UTC datetime.
    :rtype: datetime.datetime
    """
    return datetime.datetime.fromisoformat(dtstring)


def get_datetime_local():
    """
    Get current local timestamp.

    :return: Curent local timestamp.
    :rtype: datetime.datetime
    """
    return datetime.datetime.now()


def check_file_exists(filename):
    """
    Check, that given file exists in the filesystem.

    :param str filename: Name of the file to check.
    :return: Existence flag as ``True`` or ``False``.
    :rtype: bool
    """
    return os.path.isfile(filename)


def in_query_params(haystack, needles, on_true = True, on_false = False, on_empty = False):
    """
    Utility method for checking that any needle from given list of needles is
    present in given haystack.
    """
    if not haystack:
        return on_empty
    for needle in needles:
        if needle in haystack:
            return on_true
    return on_false


def generate_query_params(baseparams, updates):
    """
    Generate query parameters for GET method form.

    :param dict baseparams: Original query parameters.
    :param dict updates: Updates for query parameters.
    :return: Deep copy of original parameters modified with given updates.
    :rtype: dict
    """
    result = copy.deepcopy(baseparams)
    result.update(updates)
    return result


def parse_csv(content, delimiter):
    """
    Used to parse CSV from attachments in IDEA.
    If it is unable to parse as CSV, None is returned.

    :param str content: string from Attach.Content in IDEA message.
    :param str delimiter: delimiter used in the file (comma, tab...).
    :return Optional[List[List[str]]]: list of parsed lines, or None if unable to parse.
    """
    try:
        return list(csv.reader(content.splitlines(), delimiter=delimiter))
    except Exception:
        return None


def get_uuid4():
    """
    Generate random UUID identifier.
    """
    return uuid.uuid4()


def load_json_from_file(filename):
    """
    Load JSON from given file.
    """
    with open(filename, encoding="utf8") as fhnd:
        res = json.load(fhnd)
    return res


def make_copy_deep(data):
    """
    Make a deep copy of given data structure.
    """
    return copy.deepcopy(data)


def get_format_byte_size_function(
    format_func: Callable[[float], str] = lambda x: f'{x:.4g}',
    base: int = 1024
) -> Callable[[int], str]:

    def format_byte_size(size: int) -> str:
        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]

        if size == 0:
            return f"{format_func(0.0)} B"

        exponent = min(int(math.log(abs(size), base)), len(units) - 1)
        val = size / (base ** exponent)
        return f'{format_func(val)} {units[exponent]}'

    return format_byte_size


F = TypeVar('F', bound=Callable[..., str])


def fallback_formatter(formatter: F, fallback: str = '🗙') -> F:
    """
    Returns wrapped formatter function so that when the formatter function
    fails with an exception, fallback string is returned instead.
    """
    @functools.wraps(formatter)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        try:
            return formatter(*args, **kwargs)
        except Exception:
            return fallback
    return cast(F, wrapper)
