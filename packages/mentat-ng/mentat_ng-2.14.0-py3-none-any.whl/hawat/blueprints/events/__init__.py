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
related to `IDEA <https://idea.cesnet.cz/en/index>`__ events, database searching,
viewing event details and producing event dashboards.
"""

__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

import datetime

import flask
from flask_babel import lazy_gettext
import markupsafe
import pytz

from hawat import charts
import hawat.acl
from hawat.base import HawatBlueprint, PsycopgMixin
from hawat.blueprints.event_classes import get_event_class
from hawat.blueprints.events.forms import EventDashboardForm, SimpleEventSearchForm
import hawat.const
import hawat.events
from hawat.events import get_after_cleanup
import hawat.forms
import hawat.menu
from hawat.utils import URLParamsBuilder
from hawat.view import BaseSearchView, BaseView, ItemShowView, SimpleView
from hawat.view.mixin import AJAXMixin, HTMLMixin, SQLAlchemyMixin
from mentat.const import tr_
from mentat.datatype.sqldb import EventStatisticsModel
import mentat.services.eventstorage
import mentat.stats.idea

BLUEPRINT_NAME = 'events'
"""Name of the blueprint as module global constant."""

_EVENTS_SECTION = charts.ChartSection(
    mentat.stats.idea.ST_SKEY_CNT_EVENTS,
    lazy_gettext('events'),
    lazy_gettext('Total events processed'),
    lazy_gettext(
        'This view shows total numbers of IDEA events related to given network.'
    ),
    charts.DataComplexity.NONE,
    lazy_gettext('Total events')
)
_AGG_SECTIONS = [charts.COMMON_CHART_SECTIONS_MAP[key] for key in (
    mentat.stats.idea.ST_SKEY_ANALYZERS,
    mentat.stats.idea.ST_SKEY_ASNS,
    mentat.stats.idea.ST_SKEY_CATEGORIES,
    mentat.stats.idea.ST_SKEY_CATEGSETS,
    mentat.stats.idea.ST_SKEY_COUNTRIES,
    mentat.stats.idea.ST_SKEY_DETECTORS,
    mentat.stats.idea.ST_SKEY_DETECTORSWS,
    mentat.stats.idea.ST_SKEY_SOURCES,
    mentat.stats.idea.ST_SKEY_TARGETS,
    mentat.stats.idea.ST_SKEY_CLASSES,
    mentat.stats.idea.ST_SKEY_SEVERITIES
)]

# only include abuses in overall and internal statistics.
DASHBOARD_CHART_SECTIONS = [
    _EVENTS_SECTION,
    charts.COMMON_CHART_SECTIONS_MAP[mentat.stats.idea.ST_SKEY_ABUSES]
] + _AGG_SECTIONS
DASHBOARD_CHART_SECTIONS_EXTERNAL = _AGG_SECTIONS


def _get_search_form(request_args=None):
    choices = hawat.events.get_event_form_choices()

    form = SimpleEventSearchForm(
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
    )

    # In case no time bounds were set adjust them manually.
    if request_args and not (
            'dt_from' in request_args or 'dt_to' in request_args or 'st_from' in request_args or 'st_to' in request_args):
        form.dt_from.process_data(hawat.forms.default_dt_with_delta())
        form.dt_to.process_data(hawat.forms.default_dt())

    return form


def _group_to_group_name(group):
    if isinstance(group, str):
        return group
    return group.name


class AbstractSearchView(PsycopgMixin, BaseSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for all views responsible for searching `IDEA <https://idea.cesnet.cz/en/index>`__
    event database.
    """
    authentication = True

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Search event database')

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(cls.module_name)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Events')

    @staticmethod
    def get_search_form(request_args):
        return _get_search_form(request_args)

    def do_before_search(self, form_data):  # pylint: disable=locally-disabled,unused-argument
        form_data['groups'] = [_group_to_group_name(item) for item in form_data['groups']]
        form_data['target_groups'] = [_group_to_group_name(item) for item in form_data['target_groups']]

        from_time = form_data['st_from'] or form_data['dt_from']  # It is possible both are defined

        if from_time is None:
            is_after_cleanup = True
        else:
            is_after_cleanup = get_after_cleanup(from_time)

        self.response_context.update(
            after_cleanup=is_after_cleanup
        )

    def do_before_response(self, **kwargs):
        self.response_context.update(
            quicksearch_list=self.get_quicksearch_by_time()
        )


class SearchView(HTMLMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for searching the `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of HTML page.
    """
    methods = ['GET']

    has_help = True

    @staticmethod
    def get_qtype():
        """
        Get type of the event select query.
        """
        return mentat.services.eventstorage.QTYPE_SELECT_GHOST

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

    @classmethod
    def get_context_action_menu(cls):
        action_menu = hawat.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint='events.show',
            hidetitle=True
        )
        action_menu.add_entry(
            'endpoint',
            'download',
            endpoint='events.download',
            hidetitle=True
        )
        return action_menu


class APISearchView(AJAXMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for searching the `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of JSON document.
    """
    methods = ['GET', 'POST']

    @classmethod
    def get_view_name(cls):
        return 'apisearch'


class AbstractShowView(PsycopgMixin, ItemShowView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class responsible for fetching and presenting single `IDEA <https://idea.cesnet.cz/en/index>`__
    event.
    """
    authentication = True

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Show event')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Show')

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'View details of event &quot;%(item)s&quot;',
            item=markupsafe.escape(kwargs['item'].get_id())
        )


class ShowView(HTMLMixin, AbstractShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Detailed `IDEA <https://idea.cesnet.cz/en/index>`__ event view that presents
    the result as HTML page.
    """
    methods = ['GET']

    has_help = True

    @classmethod
    def get_action_menu(cls):  # pylint: disable=locally-disabled,unused-argument
        action_menu = hawat.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'json',
            endpoint='events.json'
        )
        action_menu.add_entry(
            'endpoint',
            'download',
            endpoint='events.download'
        )
        action_menu.add_entry(
            'endpoint',
            'playground',
            endpoint='filters.playground',
            url=lambda **x: flask.url_for('filters.playground', event_id=x['item'].get_id()),
        )
        return action_menu

    def do_before_response(self, **kwargs):
        self.response_context.update(
            get_event_class=get_event_class
        )


class APIShowView(AJAXMixin, AbstractShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Detailed `IDEA <https://idea.cesnet.cz/en/index>`__ event view that presents
    the result as HTML page.
    """
    methods = ['GET', 'POST']

    @classmethod
    def get_view_name(cls):
        return 'apishow'


class JSONShowView(HTMLMixin, PsycopgMixin, ItemShowView):  # pylint: disable=locally-disabled,abstract-method
    """
    Presenting idea `IDEA <https://idea.cesnet.cz/en/index>`__ event as the original JSON.
    """
    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'json'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Show event as JSON')

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Show as JSON')

    @classmethod
    def get_view_template(cls):
        return '{}/{}.html'.format(cls.module_name, cls.get_view_name())

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'View JSON of event &quot;%(item)s&quot;',
            item=markupsafe.escape(kwargs['item'].get_id())
        )

    @classmethod
    def get_action_menu(cls):  # pylint: disable=locally-disabled,unused-argument
        action_menu = hawat.menu.Menu()
        action_menu.add_entry(
            'endpoint',
            'json',
            endpoint='events.show'
        )
        action_menu.add_entry(
            'endpoint',
            'download',
            endpoint='events.download'
        )
        action_menu.add_entry(
            'endpoint',
            'playground',
            endpoint='filters.playground',
            url=lambda **x: flask.url_for('filters.playground', event_id=x['item'].get_id()),
        )
        return action_menu


class DownloadView(PsycopgMixin, BaseView):
    """
    Download `IDEA <https://idea.cesnet.cz/en/index>`__ event as JSON file.
    """
    methods = ['GET']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'download'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Download event')

    @classmethod
    def get_view_url(cls, **kwargs):
        return flask.url_for(
            cls.get_view_endpoint(),
            item_id=kwargs['item'].get_id()
        )

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Download')

    @classmethod
    def get_menu_legend(cls, **kwargs):
        return lazy_gettext(
            'Download event &quot;%(item)s&quot;',
            item=markupsafe.escape(kwargs['item'].get_id())
        )

    # ---------------------------------------------------------------------------

    def dispatch_request(self, item_id):  # pylint: disable=locally-disabled,arguments-differ
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.

        Single item with given unique identifier will be retrieved from database
        and injected into template to be displayed to the user.
        """
        item = self.fetch(item_id)
        if not item:
            flask.abort(404)

        self.logger.debug(
            "Event %s is being downloaded as a standalone file.",
            item['ID']
        )

        response = flask.make_response(
            item.to_json(indent=4, sort_keys=True)
        )
        response.mimetype = 'application/json'
        response.headers['Content-Disposition'] = 'attachment; filename={}.idea.json'.format(item_id)
        return response


class AttachmentDownloadView(HTMLMixin, PsycopgMixin, BaseView):
    """
    Download an attachment from `IDEA <https://idea.cesnet.cz/en/index>`__ event as a file.
    """
    methods = ['GET']

    authentication = True

    @classmethod
    def get_view_name(cls):
        return 'attachmentdownload'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Download attachment')

    # ---------------------------------------------------------------------------

    def dispatch_request(self, item_id, attachment_number):  # pylint: disable=locally-disabled,arguments-differ
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.
        """
        def _parse_attachment_number(number):
            try:
                return int(attachment_number)
            except ValueError:
                return None

        item = self.fetch(item_id)
        if not item:
            self.abort(404)

        attachment_number = _parse_attachment_number(attachment_number)
        if attachment_number is None:
            self.abort(400,
                lazy_gettext('Attachment number must be a valid number.'))

        attachment = item.get_attachment(attachment_number)
        if not attachment:
            flask.abort(404)

        # In IDEA, FileName field is a list.
        name = ",".join(attachment.get('FileName', []))
        if not name:
            name = "attachment{}".format(attachment_number)

        self.logger.debug(
            "%s event's attachment with index %s is being downloaded as a standalone file.",
            item['ID'],
            attachment_number
        )
        attachment_content = item.get_attachment_content(attachment_number)
        if attachment_content is None:
            self.flash(lazy_gettext('Something went wrong and the content of this attachment could not be loaded. Please look at it in the JSON view.'),
                       'error')
            self.abort(500)
        else:
            content, extension, mimetype = attachment_content
            response = flask.make_response(content)
            response.mimetype = mimetype
            response.headers['Content-Disposition'] = 'attachment; filename={}.{}'.format(name, extension)
            return response


class AbstractDashboardView(SQLAlchemyMixin, BaseSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for presenting overall `IDEA <https://idea.cesnet.cz/en/index>`__
    event statistics dashboard.
    """
    authentication = True

    always_include_charts = False

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(BLUEPRINT_NAME)

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Events')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Overall event dashboards')

    @classmethod
    def get_view_template(cls):
        return '{}/{}.html'.format(cls.module_name, cls.get_view_name())

    # ---------------------------------------------------------------------------

    @property
    def dbmodel(self):
        return EventStatisticsModel

    @staticmethod
    def get_search_form(request_args):
        return EventDashboardForm(request_args, meta={'csrf': False})

    @staticmethod
    def build_query(query, model, form_args):
        # Adjust query based on lower time boudary selection.
        if 'dt_from' in form_args and form_args['dt_from']:
            query = query.filter(model.dt_from >= form_args['dt_from'])
        # Adjust query based on upper time boudary selection.
        if 'dt_to' in form_args and form_args['dt_to']:
            query = query.filter(model.dt_to <= form_args['dt_to'])

        # Return the result sorted by interval.
        return query.order_by(model.interval)

    def _add_chart_section_data(self, chsections, grp_key, stats, timeline_cfg):
        for i, chsection in enumerate(chsections):
            if chsection.key in (mentat.stats.idea.ST_SKEY_CNT_EVENTS,):
                data_format = charts.InputDataFormat.WIDE_SIMPLE
            else:
                data_format = charts.InputDataFormat.WIDE_COMPLEX

            timeline_chart_data = charts.TimelineChartData(
                stats[grp_key][mentat.stats.idea.ST_SKEY_TIMELINE],
                chsection,
                timeline_cfg,
                data_format,
                add_rest=True,
                x_axis_label_override=lazy_gettext('time')
            )
            chsection = chsection.add_data(timeline_chart_data)

            if chsection.data_complexity != charts.DataComplexity.NONE:
                secondary_chart_data = charts.SecondaryChartData(
                    stats[grp_key],
                    chsection,
                    data_format,
                    add_rest=True,
                    sort=True
                )
                chsection = chsection.add_data(secondary_chart_data)

            chsections[i] = chsection

    def do_after_search(self, items):
        self.logger.debug(
            "Calculating event dashboard overview from %d records.",
            len(items)
        )
        if items:
            dt_from = self.response_context['form_data'].get('dt_from', None)
            if not dt_from:
                dt_from = self.dbcolumn_min(self.dbmodel.dt_from)

            dt_to = self.response_context['form_data'].get('dt_to', None)
            if not dt_to:
                dt_to = datetime.datetime.utcnow()

            timeline_cfg = mentat.stats.idea.TimelineCFG.get_optimized(
                time_from=dt_from,
                time_to=dt_to,
                max_count=flask.current_app.config['HAWAT_CHART_TIMELINE_MAXSTEPS'],
                min_step_seconds=300,
                user_timezone=pytz.timezone(flask.session.get('timezone', 'UTC'))
            )

            self.response_context.update(
                statistics=mentat.stats.idea.aggregate_timeline_groups(
                    items,
                    timeline_cfg
                )
            )

            if self.always_include_charts:
                self.response_context.update(
                    chart_sections_overall=DASHBOARD_CHART_SECTIONS.copy(),
                    chart_sections_internal=DASHBOARD_CHART_SECTIONS.copy(),
                    chart_sections_external=DASHBOARD_CHART_SECTIONS_EXTERNAL.copy()
                )
                chsections_sections = (
                    self.response_context['chart_sections_internal'],
                    self.response_context['chart_sections_external'],
                    self.response_context['chart_sections_overall']
                )
                for chsections, grp_key in zip(chsections_sections, mentat.stats.idea.LIST_STAT_GROUPS):
                    self._add_chart_section_data(
                        chsections,
                        grp_key,
                        self.response_context['statistics'],
                        timeline_cfg
                    )

    def do_before_response(self, **kwargs):
        self.response_context.update(
            quicksearch_list=self.get_quicksearch_by_time()
        )


class DashboardView(HTMLMixin, AbstractDashboardView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for presenting overall `IDEA <https://idea.cesnet.cz/en/index>`__
    event statistics dashboard in the form of HTML page.
    """
    methods = ['GET']

    always_include_charts = True

    @classmethod
    def get_view_name(cls):
        return 'dashboard'


class APIDashboardView(AJAXMixin, AbstractDashboardView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for presenting overall `IDEA <https://idea.cesnet.cz/en/index>`__
    event statistics dashboard in the form of JSON document.
    """
    methods = ['GET', 'POST']

    @classmethod
    def get_view_name(cls):
        return 'apidashboard'

    def process_response_context(self):
        super().process_response_context()
        # Prevent certain response context keys to appear in final response.
        for key in ('items', 'quicksearch_list'):
            try:
                del self.response_context[key]
            except KeyError:
                pass
        return self.response_context


class APIMetadataView(AJAXMixin, SimpleView):
    """
    Application view providing access event metadata information.
    """
    authentication = True

    methods = ['GET', 'POST']

    @classmethod
    def get_view_name(cls):
        return 'metadata'

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Event metadata')

    def do_before_response(self, **kwargs):
        self.response_context.update(**hawat.events.get_event_enums())


# -------------------------------------------------------------------------------


class EventsBlueprint(HawatBlueprint):
    """Pluggable module - `IDEA <https://idea.cesnet.cz/en/index>`__ event database (*events*)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('<a href="https://idea.cesnet.cz/en/index">IDEA</a> event database')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            'dashboards.{}'.format(BLUEPRINT_NAME),
            position=10,
            view=DashboardView
        )
        app.menu_main.add_entry(
            'view',
            BLUEPRINT_NAME,
            position=140,
            view=SearchView,
            resptitle=True
        )

        def _get_upb():
            return URLParamsBuilder(
                {'submit': tr_('Search')}
            ).add_kwrule(
                'dt_from', False, True
            ).add_kwrule(
                'dt_to', False, True
            )

        # Register context search actions provided by this module.
        app.set_csag(
            hawat.const.CSAG_ABUSE,
            tr_('Search for source group <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('groups', True)
        )

        app.set_csag(
            hawat.const.CSAG_ABUSE,
            tr_('Search for target group <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('target_groups', True)
        )

        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for source <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('source_addrs', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for target <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('target_addrs', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for host <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('host_addrs', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_CATEGORY,
            tr_('Search for category <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('categories', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_CLASS,
            tr_('Search for source class <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('classes', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_CLASS,
            tr_('Search for target class <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('target_classes', True).add_kwrule('target_groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_DETECTOR,
            tr_('Search for detector <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('detectors', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_DETTYPE,
            tr_('Search for detector type <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('detector_types', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_HOSTTYPE,
            tr_('Search for source type <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('source_types', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_HOSTTYPE,
            tr_('Search for target type <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('target_types', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_HOSTTYPE,
            tr_('Search for host type <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('host_types', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_PORT,
            tr_('Search for source port <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('source_ports', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_PORT,
            tr_('Search for target port <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('target_ports', True).add_kwrule('groups', True, True)
        )
        app.set_csag(
            hawat.const.CSAG_PORT,
            tr_('Search for host port <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('host_ports', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_PROTOCOL,
            tr_('Search for protocol <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('protocols', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_SEVERITY,
            tr_('Search for source severity <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('severities', True).add_kwrule('groups', True, True)
        )

        app.set_csag(
            hawat.const.CSAG_SEVERITY,
            tr_('Search for target severity <strong>%(name)s</strong> in event database'),
            SearchView,
            _get_upb().add_rule('target_severities', True).add_kwrule('target_groups', True, True)
        )


# -------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`hawat.Hawat` and factory function. This function
    must return a valid instance of :py:class:`hawat.app.HawatBlueprint` or
    :py:class:`flask.Blueprint`.
    """

    hbp = EventsBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='/{}/static'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(SearchView, '/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(ShowView, '/{}/<item_id>/show'.format(BLUEPRINT_NAME))
    hbp.register_view_class(JSONShowView, '/{}/<item_id>/json'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DownloadView, '/{}/<item_id>/download'.format(BLUEPRINT_NAME))
    hbp.register_view_class(AttachmentDownloadView, '/{}/<item_id>/attachments/<attachment_number>/download'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DashboardView, '/{}/dashboard'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APISearchView, '/api/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIShowView, '/api/{}/<item_id>/show'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIDashboardView, '/api/{}/dashboard'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIMetadataView, '/api/{}/metadata'.format(BLUEPRINT_NAME))

    return hbp
