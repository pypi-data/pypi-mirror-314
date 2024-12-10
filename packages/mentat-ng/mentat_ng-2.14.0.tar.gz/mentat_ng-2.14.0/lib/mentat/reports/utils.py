#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Library containing reporting utilities.
"""


__author__  = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import datetime
import pprint

import pytz
from sqlalchemy import null

import mentat.const
import mentat.datatype.internal
from mentat.datatype.sqldb import FilterModel
import mentat.idea.internal


class ReportingSettings:  # pylint: disable=locally-disabled,too-many-instance-attributes
    """
    Class for custom manipulations with group reporting settings.
    """

    def __init__(self, group, sql_storage, **kwargs):
        self.group_name  = group.name
        self.filters     = self._init_filters(group, sql_storage)
        self.networks    = group.networks
        self.emails      = self._init_emails(group.settings_rep)
        self.mode        = self._init_mode(group.settings_rep.mode, **kwargs)
        self.template    = self._init_template(**kwargs)
        self.locale      = self._init_locale(group.settings_rep.locale, **kwargs)
        self.timezone    = self._init_timezone(group.settings_rep.timezone, **kwargs)
        self.timing      = self._init_timing(**kwargs)
        self.timing_cfg  = self._init_timing_cfg(group.settings_rep)
        self.redirect    = self._init_redirect(group.settings_rep.redirect, **kwargs)

    def __repr__(self):
        return 'ReportingSettings(group_name={};filters={};networks={};emails={};mode={};template={};locale={};timezone={};timing={};timing_cfg={};redirect={})'.format(
            self.group_name,
            pprint.pformat(self.filters, compact = True),
            pprint.pformat(self.networks, compact = True),
            pprint.pformat(self.emails, compact = True),
            pprint.pformat(self.mode, compact = True),
            pprint.pformat(self.template, compact = True),
            pprint.pformat(self.locale, compact = True),
            pprint.pformat(self.timezone, compact = True),
            pprint.pformat(self.timing, compact = True),
            pprint.pformat(self.timing_cfg, compact = True, width = 10000),
            pprint.pformat(self.redirect, compact = True)
        )

    @staticmethod
    def _init_filters(group, sql_storage):
        global_filters = sql_storage.session.query(FilterModel) \
            .filter(FilterModel.group == null()) \
            .all()
        return global_filters + group.filters

    @staticmethod
    def _init_emails(settings):
        return (settings.emails_info, settings.emails_low, settings.emails_medium, settings.emails_high, settings.emails_critical)

    @staticmethod
    def _init_mode(group_value, **kwargs):
        if 'force_mode' in kwargs and kwargs['force_mode'] is not None:
            if kwargs['force_mode'] not in mentat.const.REPORTING_MODES:
                raise ValueError("Invalid value '{:s}' for reporting mode.".format(kwargs['force_mode']))
            return str(kwargs['force_mode'])
        if group_value is not None:
            return group_value
        return mentat.const.DFLT_REPORTING_MODE

    @staticmethod
    def _init_template(**kwargs):
        if 'force_template' in kwargs and kwargs['force_template'] is not None:
            return str(kwargs['force_template'])
        return mentat.const.DFLT_REPORTING_TEMPLATE

    @staticmethod
    def _init_locale(group_value, **kwargs):
        if 'force_locale' in kwargs and kwargs['force_locale'] is not None:
            return str(kwargs['force_locale'])
        if group_value is not None:
            return group_value
        return mentat.const.DFLT_REPORTING_LOCALE

    @staticmethod
    def _init_timezone(group_value, **kwargs):
        if 'force_timezone' in kwargs and kwargs['force_timezone'] is not None:
            if kwargs['force_timezone'] not in pytz.common_timezones:
                raise ValueError("Invalid value '{}' for reporting timezone. Please use one of the values defined in pytz.common_timezones package.".format(kwargs['force_timezone']))
            return str(kwargs['force_timezone'])
        if group_value is not None:
            return group_value
        return mentat.const.DFLT_REPORTING_TIMEZONE

    @staticmethod
    def _init_redirect(group_value, **kwargs):
        if 'force_redirect' in kwargs and kwargs['force_redirect'] is not None:
            return bool(kwargs['force_redirect'])
        if group_value is not None:
            return group_value
        return mentat.const.DFLT_REPORTING_REDIRECT

    @staticmethod
    def _init_timing(**kwargs):
        if 'force_timing' in kwargs and kwargs['force_timing'] is not None:
            if kwargs['force_timing'] not in mentat.const.REPORTING_TIMINGS:
                raise ValueError("Invalid value '{}' for reporting timing.".format(kwargs['force_timing']))
            return str(kwargs['force_timing'])
        return mentat.const.DFLT_REPORTING_TIMING

    @staticmethod
    def _init_timing_cfg(settings_rep):
        return {
            mentat.const.EVENT_SEVERITY_INFO: {
                'per': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_INFO_PER]
                ),
                'thr': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_INFO_THR]
                ),
                'thr_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_INFO_THR]
                ),
                'rel': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_INFO_REL]
                ),
                'rel_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_INFO_REL]
                )
            },
            mentat.const.EVENT_SEVERITY_LOW: {
                'per': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_LOW_PER]
                ),
                'thr': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_LOW_THR]
                ),
                'thr_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_LOW_THR]
                ),
                'rel': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_LOW_REL]
                ),
                'rel_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_LOW_REL]
                )
            },
            mentat.const.EVENT_SEVERITY_MEDIUM: {
                'per': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_MEDIUM_PER]
                ),
                'thr': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_MEDIUM_THR]
                ),
                'thr_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_MEDIUM_THR]
                ),
                'rel': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_MEDIUM_REL]
                ),
                'rel_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_MEDIUM_REL]
                )
            },
            mentat.const.EVENT_SEVERITY_HIGH: {
                'per': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_HIGH_PER]
                ),
                'thr': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_HIGH_THR]
                ),
                'thr_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_HIGH_THR]
                ),
                'rel': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_HIGH_REL]
                ),
                'rel_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_HIGH_REL]
                )
            },
            mentat.const.EVENT_SEVERITY_CRITICAL: {
                'per': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_CRITICAL_PER]
                ),
                'thr': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_CRITICAL_THR]
                ),
                'thr_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_CRITICAL_THR]
                ),
                'rel': datetime.timedelta(
                    seconds = mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_DEFAULT_CRITICAL_REL]
                ),
                'rel_target': datetime.timedelta(
                    seconds=mentat.const.REPORTING_INTERVALS[mentat.const.REPORTING_TIMING_TARGET_CRITICAL_REL]
                )
            }
        }

    def setup_filters(self, flt_parser, flt_compiler, is_target):
        """
        Setup and return list of filters in format appropriate for direct filtering
        by :py:func:`mentat.reports.event.EventReporter.filter_events` function.

        :param pynspect.gparser.PynspectFilterParser flt_parser: Parser object.
        :param pynspect.compilers.IDEAFilterCompiler flt_compiler: Compiler object.
        :param bool is_target: If the reporting is target-based (or source-based if False).
                               Only target filters are applied for target-based reporting, and only
                               source (summary/extra) filters are applied for source-based reporting.
        :return: List of processed and compiled filters.
        :rtype: list
        """
        result = []
        for filter_obj in self.filters:
            if not filter_obj.enabled or not filter_obj.is_valid:
                continue
            # Check if the filter is filtering the particular type of reports.
            if filter_obj.source_based == is_target:
                continue
            flt = flt_parser.parse(filter_obj.filter)
            flt = flt_compiler.compile(flt)
            result.append((filter_obj, flt))
        return result

    def setup_networks(self):
        """
        Setup and return list of network in format appropriate for populating the
        :py:class:`mentat.services.whois.WhoisModule`.

        :return: List of processed networks.
        :rtype: list
        """
        result = []
        for net in self.networks:
            result.append(mentat.datatype.internal.t_network_record({
                'network': net.network,
                'abuse_group': self.group_name
            }))
        return result


class ThresholdingCache:
    """
    Base class for implementing event thresholding caches for periodical event
    reporting.
    """

    def event_is_thresholded(self, event, source, ttl, is_target):
        """
        Check, that given combination of event and source is thresholded within given TTL.

        :param mentat.idea.internal.Idea event: IDEA event to check.
        :param str source: Source to check.
        :param datetime.datetime ttl: TTL for the thresholding record.
        :param bool is_target: If the reporting is target-based (or source-based if False).
        :return: ``True`` in case the event is thresholded, ``False`` otherwise.
        :rtype: bool
        """
        cachekey = self._generate_cache_key(event, source, is_target)
        return self.check(cachekey, ttl)

    def set_threshold(self, event, source, thresholdtime, relapsetime, ttl, is_target, report_label=None):
        """
        Threshold given event with given TTL.

        :param mentat.idea.internal.Idea event: IDEA event to threshold.
        :param str source: Source address because of which to threshold the event.
        :param datetime.datetime thresholdtime: Threshold window start time.
        :param datetime.datetime relapsetime: Relapse window start time.
        :param datetime.datetime ttl: Record TTL.
        :param bool is_target: If the reporting is target-based (or source-based if False).
        :param str report_label: Label of the report in which source address was reported.
        """
        cachekey = self._generate_cache_key(event, source, is_target)
        self.set(cachekey, thresholdtime, relapsetime, ttl, report_label)

    def threshold_event(self, event, source, group_name, severity, createtime, is_target):
        """
        Threshold given event with given TTL.

        :param mentat.idea.internal.Idea event: IDEA event to threshold.
        :param str source: Source address because of which to threshold the event.
        :param str group_name: Name of the group for which to threshold.
        :param str severity: Event severity.
        :param datetime.datetime createtime: Thresholding timestamp.
        :param bool is_target: If the reporting is target-based (or source-based if False).
        """
        cachekey = self._generate_cache_key(event, source, is_target)
        self.save(event.get_id(), cachekey, group_name, severity, createtime, is_target)

    #---------------------------------------------------------------------------

    def check(self, key, ttl):
        """
        Check event thresholding cache for given key and TTL. This method always
        returns ``False``.

        :param str key: Thresholding cache key.
        :param datetime.datetime ttl: Cache record TTL.
        :return: ``True`` if given key was found with valid TTL,``False`` othrewise.
        :rtype: bool
        """
        raise NotImplementedError()

    def set(self, key, thresholdtime, relapsetime, ttl, report_label=None):
        """
        Set thresholding cache record with given key and TTL.

        :param str key: Thresholding cache key.
        :param datetime.datetime thresholdtime: Threshold window start time.
        :param datetime.datetime relapsetime: Relapse window start time.
        :param datetime.datetime ttl: Record TTL.
        :param str report_label: Label of the report in which source address was reported.
        """
        raise NotImplementedError()

    def save(self, event_id, key_id, group_name, severity, createtime, is_target):
        """
        Save event into registry of thresholded events.

        :param str event_id: Event ID.
        :param str key_id: Thresholding cache key.
        :param datetime.datetime createtime: Time of the thresholding.
        :param bool is_target: If the reporting is target-based (or source-based if False).
        """
        raise NotImplementedError()

    def relapses(self, group_name, severity, ttl, is_target):
        """
        Search for list of relapsed events for given group and severity.

        :param str group_name: Name of the group.
        :param str severity: Event severity.
        :param datetime.datetime ttl: Record TTL time.
        :param bool is_target: If the reporting is target-based (or source-based if False).
        :return: Touple with list of relapsed events as :py:class:`mentat.idea.internal.Idea` objects and their aggregation by keyid.
        :rtype: touple
        """
        raise NotImplementedError()

    def cleanup(self, ttl):
        """
        Cleanup records from thresholding cache with TTL older than given value.

        :param datetime.datetime ttl: Record TTL cleanup threshold.
        """
        raise NotImplementedError()

    #---------------------------------------------------------------------------

    def _generate_cache_key(self, event, source, is_target):
        """
        Generate cache key for given event and source.

        :param mentat.idea.internal.Idea event: Event to process.
        :param str source: Source to process.
        :param bool is_target: If the reporting is target-based (or source-based if False).
        :return: Cache key as strings.
        :rtype: str
        """
        idea = mentat.idea.internal.Idea(event)
        event_class = idea.get_whole_target_class() if is_target else idea.get_whole_class()
        if not event_class:
            event_class = '/'.join(idea.get_categories())
        return '+++'.join((event_class, str(source)))

    def get_source_from_cache_key(self, key):
        """
        Return source from which was key generated.

        :param str key: Cache key.
        :return: Cached source.
        :rtype: str
        """
        return key.split('+++')[1] if key and len(key.split('+++')) > 1 else key


class NoThresholdingCache(ThresholdingCache):
    """
    Implementation of the :py:class:`mentat.reports.utils.ThresholdingCache` that
    does no thresholding at all. It can be used to disable the thresholding feature
    during reporting, for example for generating some kind of ad-hoc reports.
    """
    def check(self, key, ttl):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.check` method.
        """
        return False

    def set(self, key, thresholdtime, relapsetime, ttl, report_label=None):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.set` method.
        """
        return

    def save(self, event_id, key_id, group_name, severity, createtime, is_target):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.save` method.
        """
        return

    def relapses(self, group_name, severity, ttl, is_target):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.relapses` method.
        """
        return []

    def cleanup(self, ttl):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.cleanup` method.
        """
        return {'thresholds': 0, 'events': 0}


class SimpleMemoryThresholdingCache(ThresholdingCache):
    """
    Implementation of the :py:class:`mentat.reports.utils.ThresholdingCache` that
    performs thresholding within the memory structures.
    """

    def __init__(self):
        self.memcache = {}

    def check(self, key, ttl):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.check` method.
        """
        return bool(key in self.memcache)

    def set(self, key, thresholdtime, relapsetime, ttl, report_label=None):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.set` method.
        """
        self.memcache[key] = True

    def save(self, event_id, key_id, group_name, severity, createtime, is_target):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.save` method.
        """
        return

    def relapses(self, group_name, severity, ttl, is_target):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.relapses` method.
        """
        return []

    def cleanup(self, ttl):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.cleanup` method.
        """
        result = {
            'thresholds': len(self.memcache),
            'events': 0
        }
        self.memcache = {}
        return result


class SingleSourceThresholdingCache(SimpleMemoryThresholdingCache):
    """
    Implementation of the :py:class:`mentat.reports.utils.ThresholdingCache` that
    performs thresholding within the memory structures.
    """

    def __init__(self, source):
        super().__init__()
        self.source = source

    def _generate_cache_key(self, event, source, is_target):
        """
        Generate cache key for given event and source.

        :param mentat.idea.internal.Idea event: Event to process.
        :param str source: Source to process.
        :param bool is_target: If the reporting is target-based (or source-based if False).
        :return: Cache key as strings.
        :rtype: str
        """
        return super()._generate_cache_key(event, self.source, is_target)


class StorageThresholdingCache(ThresholdingCache):
    """
    Implementation of the :py:class:`mentat.reports.utils.ThresholdingCache` that
    is using :py:class:`mentat.services.eventstorage` service for storing thresholding
    records.
    """

    def __init__(self, logger, eventservice):
        self.logger               = logger
        self.eventservice         = eventservice
        self.memcache_thresholded = {}
        self.memcache_set         = {}

    def check(self, key, ttl):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.check` method.
        """
        if key not in self.memcache_thresholded:
            result = self.eventservice.threshold_check(key, ttl)
            self.memcache_thresholded[key] = bool(result)
        return self.memcache_thresholded[key]

    def set(self, key, thresholdtime, relapsetime, ttl, report_label=None):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.set` method.
        """
        if key not in self.memcache_set or not self.memcache_set[key]:
            try:
                self.eventservice.threshold_set(key, thresholdtime, relapsetime, ttl, report_label)
                self.logger.info(
                    "Updated thresholding cache with record - TTL=%s|RLP=%s|THR=%s|KEY=%s",
                    ttl.isoformat(),
                    relapsetime.isoformat(),
                    thresholdtime.isoformat(),
                    key
                )
            except mentat.services.eventstorage.StorageIntegrityError:
                self.logger.info(
                    "Prolonged thresholding cache record - TTL=%s|RLP=%s|THR=%s|KEY=%s",
                    ttl.isoformat(),
                    relapsetime.isoformat(),
                    thresholdtime.isoformat(),
                    key
                )
            self.memcache_thresholded[key] = True
            self.memcache_set[key] = True

    def save(self, event_id, key_id, group_name, severity, createtime, is_target):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.save` method.
        """
        try:
            self.eventservice.threshold_save(event_id, key_id, group_name, severity, createtime, is_target)
            self.logger.info(
                "Recorded thresholded event with record - CT=%s|KEY=%s|EID=%s|GRP=%s|SEV=%s|istarget=%s",
                createtime.isoformat(),
                key_id,
                event_id,
                group_name,
                severity,
                is_target
            )
        except mentat.services.eventstorage.StorageIntegrityError:
            self.logger.info(
                "Event is already thresholded with record - CT=%s|KEY=%s|EID=%s|GRP=%s|SEV=%s|istarget=%s",
                createtime.isoformat(),
                key_id,
                event_id,
                group_name,
                severity,
                is_target
            )

    def relapses(self, group_name, severity, ttl, is_target):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.relapses` method.
        """
        return self.eventservice.search_relapsed_events(group_name, severity, ttl, is_target)

    def cleanup(self, ttl):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.reports.utils.ThresholdingCache.cleanup` method.
        """
        self.memcache_thresholded = {}
        self.memcache_set = {}

        count_tc = self.eventservice.thresholds_clean(ttl)
        self.logger.info(
            "Cleaned %d records from thresholding cache older than %s.",
            count_tc,
            ttl.isoformat()
        )
        count_te = self.eventservice.thresholded_events_clean()
        self.logger.info(
            "Cleaned %d records from registry of thresholded events.",
            count_te,
        )
        return { 'thresholds': count_tc, 'events': count_te }
