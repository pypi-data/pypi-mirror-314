#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
# -------------------------------------------------------------------------------


"""
This file contains pluggable module for Hawat web interface containing features
related to `IDEA <https://idea.cesnet.cz/en/index>`__ event timeline based
visualisations.
"""

__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

from collections.abc import Sequence
import copy
import datetime
from itertools import takewhile

import flask
from flask_babel import lazy_gettext
import pytz

from hawat import charts
import hawat.acl
from hawat.base import HawatBlueprint, PsycopgMixin
from hawat.blueprints.timeline.forms import SimpleTimelineSearchForm, SimpleTimelineTabSearchForm
import hawat.const
import hawat.events
from hawat.events import get_after_cleanup
import hawat.forms
import hawat.menu
from hawat.utils import URLParamsBuilder
from hawat.view import BaseSearchView, CustomSearchView
from hawat.view.mixin import AJAXMixin, HTMLMixin
from mentat.const import tr_
import mentat.services.eventstorage
from mentat.services.eventstorage import QTYPE_TIMELINE
import mentat.stats.idea
from mentat.stats.idea import TimeBoundType, TimelineCFG

BLUEPRINT_NAME = 'timeline'
"""Name of the blueprint as module global constant."""

AGGREGATIONS: Sequence[tuple[str, dict, dict]] = (
    (mentat.stats.idea.ST_SKEY_CNT_EVENTS, {}, {"aggr_set": None}),
    (mentat.stats.idea.ST_SKEY_CATEGORIES, {}, {"aggr_set": "category"}),
    (mentat.stats.idea.ST_SKEY_SOURCES, {}, {"aggr_set": "source_ip"}),
    (mentat.stats.idea.ST_SKEY_TARGETS, {}, {"aggr_set": "target_ip"}),
    (mentat.stats.idea.ST_SKEY_SRCPORTS, {}, {"aggr_set": "source_port"}),
    (mentat.stats.idea.ST_SKEY_TGTPORTS, {}, {"aggr_set": "target_port"}),
    (mentat.stats.idea.ST_SKEY_SRCTYPES, {}, {"aggr_set": "source_type"}),
    (mentat.stats.idea.ST_SKEY_TGTTYPES, {}, {"aggr_set": "target_type"}),
    (mentat.stats.idea.ST_SKEY_PROTOCOLS, {}, {"aggr_set": "protocol"}),
    (mentat.stats.idea.ST_SKEY_DETECTORS, {}, {"aggr_set": "node_name"}),
    (mentat.stats.idea.ST_SKEY_DETECTORTPS, {}, {"aggr_set": "node_type"}),
    (mentat.stats.idea.ST_SKEY_ABUSES, {}, {"aggr_set": "resolvedabuses"}),
    (mentat.stats.idea.ST_SKEY_CLASSES, {}, {"aggr_set": "eventclass"}),
    (mentat.stats.idea.ST_SKEY_SEVERITIES, {}, {"aggr_set": "eventseverity"}),
    (mentat.stats.idea.ST_SKEY_DESCRIPTION, {}, {"aggr_set": "description"}),
)

TIMELINE_CHART_SECTIONS = [
    charts.ChartSection(
        mentat.stats.idea.ST_SKEY_CNT_EVENTS,
        lazy_gettext('events'),
        lazy_gettext('Total event counts'),
        lazy_gettext(
            'This view shows total numbers of IDEA events related to given network.'
        ),
        charts.DataComplexity.NONE,
        lazy_gettext('Total events'),
    ),
] + [charts.COMMON_CHART_SECTIONS_MAP[key] for key, _, _ in AGGREGATIONS if key in charts.COMMON_CHART_SECTIONS_MAP] + [
    charts.ChartSection(
        mentat.stats.idea.ST_SKEY_DESCRIPTION,
        lazy_gettext('descriptions'),
        lazy_gettext('Event descriptions'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to <em>event '
            'description</em>.'
        ),
        charts.DataComplexity.SINGLE,
        lazy_gettext('Description'),
    )
]


def _get_search_form(request_args=None, form_cls=SimpleTimelineSearchForm):
    choices = hawat.events.get_event_form_choices()
    aggrchc = list(
        zip(
            map(lambda x: x[0], AGGREGATIONS),
            map(lambda x: x[0], AGGREGATIONS)
        )
    )
    sectionchc = [(mentat.stats.idea.ST_SKEY_CNT_EVENTS, mentat.stats.idea.ST_SKEY_CNT_EVENTS)] + aggrchc

    form = form_cls(
        request_args,
        meta={'csrf': False},
        choices_source_types=choices['source_types'],
        choices_target_types=choices['target_types'],
        choices_host_types=choices['host_types'],
        choices_detectors=choices['detectors'],
        choices_detector_types=choices['detector_types'],
        choices_categories=choices['categories'],
        choices_severities=choices['severities'],
        choices_target_severities=choices['target_severities'],
        choices_classes=choices['classes'],
        choices_target_classes=choices['target_classes'],
        choices_protocols=choices['protocols'],
        choices_inspection_errs=choices['inspection_errs'],
        choices_sections=sectionchc,
        choices_aggregations=aggrchc
    )

    # In case no time bounds were set adjust them manually.
    if request_args and not ('dt_from' in request_args or 'dt_to' in request_args or 'st_from' in request_args or 'st_to' in request_args):
        form.dt_from.process_data(hawat.forms.default_dt_with_delta())
        form.dt_to.process_data(hawat.forms.default_dt())
    elif request_args:
        if 'dt_from' not in request_args:
            form.dt_from.process_data(None)
        if 'dt_to' not in request_args:
            form.dt_to.process_data(None)
        if 'st_from' not in request_args:
            form.st_from.process_data(None)
        if 'st_to' not in request_args:
            form.st_to.process_data(None)

    return form


def _group_to_group_name(group):
    if isinstance(group, str):
        return group
    return group.name


class AbstractSearchView(PsycopgMixin, CustomSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for view responsible for searching `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in timeline-based manner.
    """
    authentication = True

    url_params_unsupported = ('page', 'sortby')

    always_include_charts = False

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(cls.module_name)

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Search event timeline')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Timeline')

    @staticmethod
    def get_search_form(request_args):
        return _get_search_form(request_args)

    def _set_time_bounds(self, form_data):
        """
        Based on provided form data, appropriately sets time bounds for the search,
        and returns the timeline time type.
        Times are converted to UTC naive timestamps.
        """
        if not any(form_data.get(t, None) for t in TimeBoundType.STORAGE_TIME.value):
            # if no st_* bound is defined
            time_type = TimeBoundType.DETECTION_TIME
        elif not any(form_data.get(t, None) for t in TimeBoundType.DETECTION_TIME.value):
            # if at least one st_* and no dt_* bounds are defined
            time_type = TimeBoundType.STORAGE_TIME
        else:
            self.abort(400, tr_('Invalid time bounds provided.'))
            return TimeBoundType.NONE  # Unreachable

        t_from, t_to = time_type.value

        # Set default time bounds if not provided.
        form_data[t_from] = form_data.get(t_from, None) or hawat.forms.default_dt_with_delta()
        form_data[t_to] = form_data.get(t_to, None) or datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

        return time_type

    def do_before_search(self, form_data):  # pylint: disable=locally-disabled,unused-argument
        self.response_context.update(
            sqlqueries=[]
        )

        form_data['groups'] = [_group_to_group_name(item) for item in form_data['groups']]
        form_data['target_groups'] = [_group_to_group_name(item) for item in form_data['target_groups']]

        time_type = self._set_time_bounds(form_data)
        self.response_context['time_type'] = time_type

        bucket_size = form_data.get('bucket_size')
        time_from = form_data[time_type.value.t_from]
        time_to = form_data[time_type.value.t_to]
        user_timezone = pytz.timezone(flask.session.get('timezone', 'UTC'))

        # Determine configurations for timelines.
        if bucket_size is not None:
            timeline_cfg = TimelineCFG.get_with_step(
                time_from,
                time_to,
                bucket_size,
                user_timezone=user_timezone,
                time_type=time_type
            )
        else:
            timeline_cfg = TimelineCFG.get_optimized(
                time_from,
                time_to,
                flask.current_app.config['HAWAT_CHART_TIMELINE_MAXSTEPS'],
                user_timezone=user_timezone,
                time_type=time_type
            )

        self.response_context.update(
            timeline_cfg=timeline_cfg,
            after_cleanup=get_after_cleanup(form_data.get(time_type.value.t_from))  # Treats storage time as detect time
        )

        # Put calculated parameters together with other search form parameters.
        form_data[mentat.stats.idea.ST_SKEY_TLCFG] = timeline_cfg
        form_data.update(timeline_cfg.to_dict())

        form_data['timezone'] = flask.session.get('timezone', 'UTC')

    def _search_events_aggr(self, form_args, qtype, aggr_name, enable_toplist=True):
        if self.SEARCH_QUERY_QUOTA_CHECK:
            self._check_search_query_quota()
        self.mark_time(
            '{}_{}'.format(qtype, aggr_name),
            'begin',
            tag='search',
            label='Begin aggregation calculations "{}:{}"'.format(
                qtype,
                aggr_name
            ),
            log=True
        )
        search_result = self.get_db().search_events_aggr(
            form_args,
            qtype=qtype,
            dbtoplist=enable_toplist,
            qname=self.get_qname()
        )
        self.mark_time(
            '{}_{}'.format(qtype, aggr_name),
            'end',
            tag='search',
            label='Finished aggregation calculations "{}:{}" [yield {} row(s)]'.format(
                qtype,
                aggr_name,
                len(search_result)
            ),
            log=True
        )

        self.response_context['sqlqueries'].append(
            self.get_db().cursor.lastquery.decode('utf-8')
        )
        self.response_context['search_result']["{}:{}".format(qtype, aggr_name)] = search_result

    def get_aggregations(self, form_args):
        """
        Returns a list of aggregations which should be calculated
        """
        raise NotImplementedError()

    def custom_search(self, form_args):
        aggregations_to_calculate = self.get_aggregations(form_args)
        self.response_context.update(
            search_result={},  # Raw database query results (rows).
            aggregations=aggregations_to_calculate,  # Note all performed aggregations for further processing.
        )

        # set aggregations to be shown as tabs
        if 'aggregations' in form_args and form_args['aggregations']:
            self.response_context['chart_sections'] = [chs for chs in TIMELINE_CHART_SECTIONS if chs.key in form_args['aggregations']]
        else:
            self.response_context['chart_sections'] = TIMELINE_CHART_SECTIONS.copy()

        qtype = QTYPE_TIMELINE

        # Perform timeline aggregations and aggregation aggregations for the selected aggregations
        for aggr_name, _, faupdates in AGGREGATIONS:
            if aggr_name in aggregations_to_calculate:
                fargs = copy.deepcopy(form_args)
                fargs.update(faupdates)
                self._search_events_aggr(
                    fargs,
                    qtype,
                    aggr_name,
                    enable_toplist=aggr_name != mentat.stats.idea.ST_SKEY_CNT_EVENTS
                )

    def _get_chsection_with_data(self, key: str, chsection: charts.ChartSection) -> charts.ChartSection:
        timeline_data_iter = takewhile(
            lambda x: x.bucket is not None,
            self.response_context['search_result'][key]
        )

        data_format: charts.InputDataFormatLong
        if chsection.key == mentat.stats.idea.ST_SKEY_CNT_EVENTS:
            data_format = charts.InputDataFormat.LONG_SIMPLE
        else:
            data_format = charts.InputDataFormat.LONG_COMPLEX

        timeline_chart_data = charts.TimelineChartData(
            timeline_data_iter,
            chsection,
            self.response_context['timeline_cfg'],
            data_format
        )
        chsection = chsection.add_data(timeline_chart_data)

        if chsection.key != mentat.stats.idea.ST_SKEY_CNT_EVENTS:
            secondary_chart_data = charts.SecondaryChartData(
                self.response_context['statistics'],
                chsection,
                data_format,
                self.response_context['statistics'][mentat.stats.idea.ST_SKEY_CNT_EVENTS]
            )
            chsection = chsection.add_data(secondary_chart_data)

        return chsection

    def do_after_search(self, **kwargs):
        self.response_context.update(
            statistics={
                'timeline_cfg': self.response_context['timeline_cfg']
            }
        )

        # Convert raw database rows into dataset structures.
        self.mark_time(
            'result_convert',
            'begin',
            tag='calculate',
            label='Converting result from database rows to statistical dataset',
            log=True
        )

        chart_sections = self.response_context['chart_sections']

        for i, chsection in enumerate(chart_sections):
            key = "{}:{}".format(QTYPE_TIMELINE, chsection.key)
            if key in self.response_context['search_result']:
                mentat.stats.idea.aggregate_stats_timeline(
                    chsection.key,
                    self.response_context['search_result'][key],
                    result=self.response_context['statistics']
                )

                if self.always_include_charts:
                    chart_sections[i] = self._get_chsection_with_data(key, chsection)

        self.mark_time(
            'result_convert',
            'end',
            tag='calculate',
            label='Done converting result from database rows to statistical dataset',
            log=True
        )

        self.response_context.update(
            items_count=self.response_context['statistics'].get(mentat.stats.idea.ST_SKEY_CNT_EVENTS, 0)
        )
        self.response_context.pop('search_result', None)

    def _get_timeline_search_url(self, section):
        """Returns the search query URL with the provided section set"""
        params = self.response_context['query_params'].copy()
        params['section'] = section
        return flask.url_for(
            '{}.{}'.format(
                BLUEPRINT_NAME,
                TabView.get_view_name()
            ),
            **params
        )

    def do_before_response(self, **kwargs):
        self.response_context.update(
            quicksearch_list=self.get_quicksearch_by_time(),
            get_search_url=self._get_timeline_search_url,
        )


class SearchView(HTMLMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for querying `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of HTML page.
    """
    methods = ['GET']

    always_include_charts = True

    def get_aggregations(self, form_args):
        if 'aggregations' in form_args and form_args['aggregations']:
            return form_args['aggregations']
        if 'section' in form_args and form_args['section']:
            return [form_args['section']]
        return [mentat.stats.idea.ST_SKEY_CNT_EVENTS]

    @classmethod
    def get_breadcrumbs_menu(cls):
        breadcrumbs_menu = hawat.menu.Menu()
        breadcrumbs_menu.add_entry(
            'endpoint',
            'home',
            endpoint=flask.current_app.config['ENDPOINT_HOME']
        )
        breadcrumbs_menu.add_entry(
            'endpoint',
            'search',
            endpoint='{}.search'.format(cls.module_name)
        )
        return breadcrumbs_menu


class TabView(HTMLMixin, AbstractSearchView):

    methods = ['GET']

    always_include_charts = True
    use_alert_error = True

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.view.BaseView.get_view_name`."""
        return 'tab'

    @staticmethod
    def get_search_form(request_args):
        return _get_search_form(request_args, form_cls=SimpleTimelineTabSearchForm)

    def do_after_search(self, **kwargs):
        super().do_after_search(**kwargs)
        self.response_context.update(
            chart_section=next(
                (chs for chs in self.response_context['chart_sections'] if chs.data),
                TIMELINE_CHART_SECTIONS[0]
            )
        )

    def get_aggregations(self, form_args):
        if 'section' in form_args and form_args['section']:
            return [form_args['section']]
        return [mentat.stats.idea.ST_SKEY_CNT_EVENTS]


class APISearchView(AJAXMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for querying `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of JSON document.
    """
    methods = ['GET', 'POST']

    def get_aggregations(self, form_args):
        if 'aggregations' in form_args and form_args['aggregations']:
            return form_args['aggregations']
        if 'section' in form_args and form_args['section']:
            return [form_args['section']]
        return [a[0] for a in AGGREGATIONS]

    def get_blocked_response_context_keys(self):
        return super().get_blocked_response_context_keys() + [
            'get_search_url',
            'all_aggregations'
        ]

    @classmethod
    def get_view_name(cls):
        return 'apisearch'


# -------------------------------------------------------------------------------


class AbstractLegacySearchView(PsycopgMixin, BaseSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for view responsible for searching `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in timeline-based manner.
    """
    authentication = True

    url_params_unsupported = ('page', 'limit', 'sortby')

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(cls.module_name)

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Search event timeline')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Timeline')

    @staticmethod
    def get_search_form(request_args):
        return _get_search_form(request_args)

    def do_before_search(self, form_data):  # pylint: disable=locally-disabled,unused-argument
        form_data['groups'] = [_group_to_group_name(item) for item in form_data['groups']]

    def do_after_search(self, items):
        self.logger.debug(
            "Calculating IDEA event timeline from %d records.",
            len(items)
        )
        if items:
            dt_from = self.response_context['form_data'].get('dt_from', None)
            if not dt_from and items:
                dt_from = self.get_db().search_column_with('detecttime')
            dt_to = self.response_context['form_data'].get('dt_to', None)
            if not dt_to and items:
                dt_to = datetime.datetime.utcnow()
            self.response_context.update(
                statistics=mentat.stats.idea.evaluate_timeline_events(
                    items,
                    t_from=dt_from,
                    t_to=dt_to,
                    max_count=flask.current_app.config['HAWAT_CHART_TIMELINE_MAXSTEPS'],
                    timezone=pytz.timezone(flask.session.get('timezone', 'UTC'))
                )
            )
            self.response_context.pop('items', None)

    def do_before_response(self, **kwargs):
        self.response_context.update(
            quicksearch_list=self.get_quicksearch_by_time()
        )

    @staticmethod
    def get_qtype():
        """
        Get type of the event select query.
        """
        return mentat.services.eventstorage.QTYPE_SELECT_GHOST


class APILegacySearchView(AJAXMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for querying `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of JSON document.

    *Deprecated legacy implementation, kept only for the purposes of comparison.*
    """
    methods = ['GET', 'POST']

    @classmethod
    def get_view_name(cls):
        return 'apilegacysearch'


# -------------------------------------------------------------------------------


class TimelineBlueprint(HawatBlueprint):
    """Pluggable module - IDEA event timelines (*timeline*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('<a href="https://idea.cesnet.cz/en/index">IDEA</a> event timelines')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            BLUEPRINT_NAME,
            position=150,
            view=SearchView,
            resptitle=True
        )

        # Register context actions provided by this module.
        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for source <strong>%(name)s</strong> on IDEA event timeline'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('source_addrs', True).add_kwrule('dt_from', False,
                                                                                                  True).add_kwrule(
                'dt_to', False, True)
        )


# -------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`hawat.Hawat` and factory function. This function
    must return a valid instance of :py:class:`hawat.app.HawatBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = TimelineBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder='templates'
    )

    hbp.register_view_class(SearchView, '/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(TabView, '/{}/tab/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APISearchView, '/api/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APILegacySearchView, '/api/{}/legacysearch'.format(BLUEPRINT_NAME))

    return hbp
