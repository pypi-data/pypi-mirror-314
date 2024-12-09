#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Unit tests for :py:mod:`hawat.blueprints.event_classes`.
"""


import unittest

import hawat.const
import hawat.db
import hawat.test
from hawat.test import HawatTestCase, ItemCreateHawatTestCase
import hawat.test.fixtures
from hawat.test.fixtures import DEMO_EVENT_CLASS
from hawat.test.runner import TestRunnerMixin
from mentat.datatype.sqldb import EventClassModel


class EventClassTestMixin:
    """
    Mixin class for event class specific tests.
    """

    def event_class_get(self, event_class_name, with_app_context = False):
        """
        Get given event class.
        """
        if not with_app_context:
            return hawat.db.db_session().query(EventClassModel).filter(EventClassModel.name == event_class_name).one_or_none()
        with self.app.app_context():
            return hawat.db.db_session().query(EventClassModel).filter(EventClassModel.name == event_class_name).one_or_none()

    def event_class_save(self, event_class_object, with_app_context = False):
        """
        Update given event class.
        """
        if not with_app_context:
            hawat.db.db_session().add(event_class_object)
            hawat.db.db_session().commit()
        with self.app.app_context():
            hawat.db.db_session().add(event_class_object)
            hawat.db.db_session().commit()

    def event_class_id(self, event_class, with_app_context = False):
        """
        Get ID of given event class.
        """
        if not with_app_context:
            fobj = self.event_class_get(event_class)
            return fobj.id
        with self.app.app_context():
            fobj = self.event_class_get(event_class)
            return fobj.id


class EventClassListTestCase(TestRunnerMixin, HawatTestCase):
    """Class for testing ``event_classes.list`` endpoint."""

    def _attempt_fail(self):
        self.assertGetURL(
            '/event_classes/list',
            403
        )

    def _attempt_succeed(self):
        self.assertGetURL(
            '/event_classes/list',
            200,
            [
                b'View details of event class',
                b'Event class management',
                b'Create event class',
                b'Creation time from',
                b'Clear',
                b'Severity'
            ]
        )

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user ``user``."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user ``developer``."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user ``maintainer``."""
        self._attempt_succeed()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user ``admin``."""
        self._attempt_succeed()


class EventClassShowTestCase(EventClassTestMixin, TestRunnerMixin, HawatTestCase):
    """Base class for testing ``event_classes.show`` endpoint."""

    def _attempt_fail(self):
        ec_id = self.event_class_id(DEMO_EVENT_CLASS, True)
        self.assertGetURL(
            '/event_classes/{}/show'.format(ec_id),
            403
        )
        ec_id = self.event_class_id(DEMO_EVENT_CLASS, True)
        self.assertGetURL(
            '/event_classes/{}/show'.format(DEMO_EVENT_CLASS),
            403
        )

    def _attempt_succeed(self):
        ec_id = self.event_class_id(DEMO_EVENT_CLASS, True)
        self.assertGetURL(
            '/event_classes/{}/show'.format(ec_id),
            200,
            [
                '<h3>{}</h3>'.format(DEMO_EVENT_CLASS).encode('utf8'),
                b'<strong>Event class created:</strong>',
                b'Filter playground',
                b'State:',
                b'Changelogs',
                b'Name:'
            ]
        )
        self.assertGetURL(
            '/event_classes/{}/show'.format(DEMO_EVENT_CLASS),
            200,
            [
                '<h3>{}</h3>'.format(DEMO_EVENT_CLASS).encode('utf8'),
                b'<strong>Event class created:</strong>',
                b'Filter playground',
                b'State:',
                b'Changelogs',
                b'Name:'
            ]
        )

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_USER)
    def test_01_as_user(self):
        """
        Test access as user 'user'.
        """
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """
        Test access as user 'developer'.
        """
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """
        Test access as user 'maintainer'.
        """
        self._attempt_succeed()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """
        Test access as user 'admin'.
        """
        self._attempt_succeed()


class EventClassCreateTestCase(EventClassTestMixin, TestRunnerMixin, ItemCreateHawatTestCase):
    """Class for testing ``event_classes.create`` endpoint."""

    data_fixture = [
        ('name', 'TEST_EVENT_CLASS'),
        ('source_based', True),
        ('label_en', 'Test event class for unit testing purposes.'),
        ('label_cz', 'Testovací třída událostí.'),
        ('reference', 'https://csirt.cesnet.cz/cs/services/eventclass'),
        ('displayed_main', ['FlowCount']),
        ('displayed_source', ['Hostname']),
        ('displayed_target', ['Port']),
        ('rule', 'Category IN ["Recon.Scanning"]'),
        ('severity', 'medium'),
        ('subclassing', 'Ref'),
        ('enabled', True)
    ]

    def _attempt_fail(self):
        self.assertGetURL(
            '/event_classes/create',
            403
        )

    def _attempt_succeed(self):
        self.assertCreate(
            EventClassModel,
            '/event_classes/create',
            self.data_fixture,
            [
                b'Event class ',
                b'TEST_EVENT_CLASS',
                b'was successfully created.'
            ]
        )

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed()


class EventClassUpdateTestCase(EventClassTestMixin, TestRunnerMixin, HawatTestCase):
    """Class for testing ``event_classes.update`` endpoint."""

    def _attempt_fail(self):
        ec_id = self.event_class_id(DEMO_EVENT_CLASS, True)
        self.assertGetURL(
            '/event_classes/{}/update'.format(ec_id),
            403
        )

    def _attempt_succeed(self):
        ec_id = self.event_class_id(DEMO_EVENT_CLASS, True)
        self.assertGetURL(
            '/event_classes/{}/update'.format(ec_id),
            200,
            [
                b'Update event class details',
                b'State:',
                b'Severity',
                b'Label'
            ]
        )

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_DEVELOPER)
    def test_04_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_MAINTAINER)
    def test_05_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_ADMIN)
    def test_06_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed()


class EventClassEnableDisableTestCase(EventClassTestMixin, TestRunnerMixin, HawatTestCase):
    """Class for testing ``event_classes.enable`` and ``event_classes.disable`` endpoint."""

    def _attempt_fail(self):
        ec_id = self.event_class_id(DEMO_EVENT_CLASS, True)
        self.assertGetURL(
            '/event_classes/{}/disable'.format(ec_id),
            403
        )
        self.assertGetURL(
            '/event_classes/{}/enable'.format(ec_id),
            403
        )

    def _attempt_succeed(self):
        ec_id = self.event_class_id(DEMO_EVENT_CLASS, True)
        self.assertGetURL(
            '/event_classes/{}/disable'.format(ec_id),
            200,
            [
                b'Are you really sure you want to disable following item:'
            ]
        )
        self.assertPostURL(
            '/event_classes/{}/disable'.format(ec_id),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully disabled.'
            ]
        )
        self.assertGetURL(
            '/event_classes/{}/enable'.format(ec_id),
            200,
            [
                b'Are you really sure you want to enable following item:'
            ]
        )
        self.assertPostURL(
            '/event_classes/{}/enable'.format(ec_id),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully enabled.'
            ]
        )

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed()


class EventClassDeleteTestCase(EventClassTestMixin, TestRunnerMixin, HawatTestCase):
    """Class for testing ``event_classes.delete`` endpoint."""

    def _attempt_fail(self):
        ec_id = self.event_class_id(DEMO_EVENT_CLASS, True)
        self.assertGetURL(
            '/event_classes/{}/delete'.format(ec_id),
            403
        )

    def _attempt_succeed(self):
        ec_id = self.event_class_id(DEMO_EVENT_CLASS, True)
        self.assertGetURL(
            '/event_classes/{}/delete'.format(ec_id),
            200,
            [
                b'Are you really sure you want to permanently remove following item:'
            ]
        )
        self.assertPostURL(
            '/event_classes/{}/delete'.format(ec_id),
            {
                'submit': 'Confirm'
            },
            200,
            [
                b'was successfully and permanently deleted.'
            ]
        )

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_USER)
    def test_01_as_user(self):
        """Test access as user 'user'."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_DEVELOPER)
    def test_02_as_developer(self):
        """Test access as user 'developer'."""
        self._attempt_fail()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_MAINTAINER)
    def test_03_as_maintainer(self):
        """Test access as user 'maintainer'."""
        self._attempt_succeed()

    @hawat.test.do_as_user_decorator(hawat.const.ROLE_ADMIN)
    def test_04_as_admin(self):
        """Test access as user 'admin'."""
        self._attempt_succeed()


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()
