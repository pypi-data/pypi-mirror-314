#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
# -------------------------------------------------------------------------------


"""
This pluggable module provides unified GUI access to all modules that
add some AODS (Additional Object Data Service), such as:
* DNS
* PassiveDNS
* NERD
* GeoIP
* Group resolving
"""


__author__ = "Jakub Judiny <jakub.judiny@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

import flask
from flask_babel import lazy_gettext

import ipranges

from hawat.base import HawatBlueprint
from hawat.blueprints.host_info.forms import HostInfoSearchForm
import hawat.const
import hawat.menu
from hawat.utils import URLParamsBuilder
from hawat.view import RenderableView
from hawat.view.mixin import HTMLMixin
from mentat.const import tr_

BLUEPRINT_NAME = 'host_info'
"""Name of the blueprint as module global constant."""


def get_AODS_type(value):
    """
    Returns the correct (guessed) AODS type for the given input.
    Can return 'ip4', 'ip6' or 'host' (if it is not an IP address).
    """
    for (tconv, AODS_type) in [(ipranges.IP4, "ip4"), (ipranges.IP6, "ip6")]:
        try:
            tconv(value)
            return AODS_type
        except ValueError:
            pass
    return "host"


class AbstractSearchView(RenderableView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for view responsible for searching information about a host.
    """
    authentication = True

    @classmethod
    def get_menu_title(cls, **kwargs):
        return lazy_gettext('Host info')

    @classmethod
    def get_view_title(cls, **kwargs):
        return lazy_gettext('Search host info')

    @classmethod
    def get_view_icon(cls):
        return 'module-{}'.format(BLUEPRINT_NAME).replace('_', '-')

    @staticmethod
    def get_search_form(request_args):
        return HostInfoSearchForm(
            request_args,
            meta={'csrf': False}
        )

    def dispatch_request(self):
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.
        """
        form = self.get_search_form(flask.request.args)
        if hawat.const.FORM_ACTION_SUBMIT in flask.request.args:
            if form.validate():
                form_data = form.data
                self.response_context.update(
                    searched=True,
                    form_data=form_data,
                    get_AODS_type=get_AODS_type
                )

        self.response_context.update(
            search_form=form,
            request_args=flask.request.args
        )
        return self.generate_response()


class SearchView(HTMLMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for presenting the host info search results
    in the form of HTML page.
    """
    methods = ['GET']

    @classmethod
    def get_view_name(cls):
        return 'search'


# -------------------------------------------------------------------------------


class HostInfoBlueprint(HawatBlueprint):
    """Pluggable module - Host info (host_info)."""

    @classmethod
    def get_module_title(cls):
        return lazy_gettext('Host info')

    def register_app(self, app):
        app.menu_main.add_entry(
            'view',
            '{}'.format(BLUEPRINT_NAME),
            position=250,
            view=SearchView
        )

        # Register context actions provided by this module.
        app.set_csag(
            hawat.const.CSAG_ADDRESS,
            tr_('Search for address <strong>%(name)s</strong> in Host info module'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('search')
        )
        app.set_csag(
            hawat.const.CSAG_HOSTNAMES,
            tr_('Search for hostname <strong>%(name)s</strong> in Host info module'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('search')
        )


# -------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface for :py:mod:`hawat.Hawat` and factory function. This function
    must return a valid instance of :py:class:`hawat.app.HawatBlueprint` or
    :py:class:`flask.Blueprint`.
    """
    hbp = HostInfoBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder='templates'
    )

    hbp.register_view_class(SearchView, '/{}/search'.format(BLUEPRINT_NAME))
    return hbp
