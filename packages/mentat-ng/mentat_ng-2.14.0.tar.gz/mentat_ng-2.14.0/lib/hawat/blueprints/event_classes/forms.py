#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
# -------------------------------------------------------------------------------


"""
This module contains event class management forms for Hawat.
"""

__author__ = "Jakub Judiny <jakub.judiny@cesnet.cz>"
__credits__ = "Jan Mach <jan.mach@cesnet.cz>, Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

from flask_babel import gettext, lazy_gettext
import wtforms

import pynspect.gparser

import hawat.db
import hawat.forms
import mentat.const
from mentat.datatype.sqldb import EventClassModel
from mentat.idea.internal import IDEAFilterCompiler


def check_event_class_name_uniqueness(form, field):
    """
    Callback for validating event class name uniqueness during update action.
    """
    item = hawat.db.db_get().session.query(EventClassModel). \
        filter(EventClassModel.name == field.data). \
        filter(EventClassModel.id != form.db_item_id). \
        all()
    if not item:
        return
    raise wtforms.validators.ValidationError(gettext('Event class with this name already exists.'))


def check_filter(_form, field):  # pylint: disable=locally-disabled,unused-argument
    """
    Callback for validating Pynspect filter.
    """
    psr = pynspect.gparser.PynspectFilterParser()
    psr.build()
    compiler = IDEAFilterCompiler()
    try:
        rule = psr.parse(field.data)
        compiler.compile(rule)
    except Exception as err:
        raise wtforms.validators.ValidationError(
            gettext(
                'Filtering rule parse error: "%(error)s".',
                error=str(err)
            )
        )


def check_optional_filter(_form, field):
    """
    Callback for validating optional Pynspect filter.
    """
    if field.data:
        check_filter(_form, field)


# -------------------------------------------------------------------------------


class BaseEventClassForm(hawat.forms.BaseItemForm):
    """
    Class representing base event class form.
    """
    source_based = wtforms.RadioField(
        lazy_gettext('Type:'),
        validators=[
            wtforms.validators.InputRequired(),
        ],
        choices=[
            (True, lazy_gettext('Source-based')),
            (False, lazy_gettext('Target-based'))
        ],
        default=(True, lazy_gettext('Source-based')),
        filters=[hawat.forms.str_to_bool],
        coerce=hawat.forms.str_to_bool
    )
    label_en = wtforms.TextAreaField(
        lazy_gettext('Label (en):'),
        validators=[
            wtforms.validators.DataRequired(),
        ]
    )
    label_cz = wtforms.TextAreaField(
        lazy_gettext('Label (cz):'),
        validators=[
            wtforms.validators.DataRequired(),
        ]
    )
    reference = wtforms.TextAreaField(
        lazy_gettext('Reference:'),
        validators=[
            wtforms.validators.Optional(),
        ]
    )

    displayed_main = wtforms.SelectMultipleField(
        lazy_gettext('Displayed main fields:'),
        validators=[
            wtforms.validators.Optional(),
        ],
        choices=[(a, a) for a, b in (mentat.const.REPORT_FIELDS_MAIN_NUMBER + mentat.const.REPORT_FIELDS_MAIN_LIST_VIEW)],
        default=[a for a, b in (mentat.const.REPORT_FIELDS_MAIN_NUMBER[:4] + mentat.const.REPORT_FIELDS_MAIN_LIST_VIEW[-1:])],
        filters=[lambda x: x or []],
        description=lazy_gettext(
            'These main fields will be displayed in the "Additional information" section in the reports regarding this event class.')
    )
    displayed_source = wtforms.SelectMultipleField(
        lazy_gettext('Displayed source fields:'),
        validators=[
            wtforms.validators.Optional(),
        ],
        choices=[(a, a) for a, b in (mentat.const.REPORT_FIELDS_SOURCE_LIST + mentat.const.REPORT_FIELDS_SOURCE_NUMBER_VIEW)],
        default=[a for a, b in mentat.const.REPORT_FIELDS_SOURCE_LIST[:3]],
        filters=[lambda x: x or []],
        description=lazy_gettext(
            'These source fields will be displayed in the "Additional information" section in the reports regarding this event class.')
    )
    displayed_target = wtforms.SelectMultipleField(
        lazy_gettext('Displayed target fields:'),
        validators=[
            wtforms.validators.Optional(),
        ],
        choices=[(a, a) for a, b in (mentat.const.REPORT_FIELDS_TARGET_LIST_VIEW + mentat.const.REPORT_FIELDS_TARGET_NUMBER_VIEW)],
        default=[a for a, b in mentat.const.REPORT_FIELDS_TARGET_LIST_VIEW[:1]],
        filters=[lambda x: x or []],
        description=lazy_gettext(
            'These target fields will be displayed in the "Additional information" section in the reports regarding this event class.')
    )

    rule = wtforms.TextAreaField(
        lazy_gettext('Rule:'),
        validators=[
            wtforms.validators.DataRequired(),
            check_filter
        ],
        description=lazy_gettext(
            'Events matching this rule will be assigned this event class. The same notation as in mentat-inspector can be used here.')
    )
    severity = wtforms.SelectField(
        lazy_gettext('Severity:'),
        validators=[
            wtforms.validators.DataRequired(),
        ],
        choices=[ (severity, severity) for severity in mentat.const.REPORT_SEVERITIES ],
        default="low",
        description=lazy_gettext(
            'Specification of event severity for this event class. Severity can be used during incident handling workflows to prioritize events.')
    )
    subclassing = wtforms.TextAreaField(
        lazy_gettext('Subclassing:'),
        validators=[
            check_optional_filter
        ],
        description=lazy_gettext(
            "Rule that will derive subclass for events in this event class. "
            "Blank rule means subclassing is disabled for this event class."
        )
    )

    enabled = wtforms.RadioField(
        lazy_gettext('State:'),
        validators=[
            wtforms.validators.InputRequired(),
        ],
        choices=[
            (True, lazy_gettext('Enabled')),
            (False, lazy_gettext('Disabled'))
        ],
        filters=[hawat.forms.str_to_bool],
        coerce=hawat.forms.str_to_bool
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Submit')
    )
    preview = wtforms.SubmitField(
        lazy_gettext('Preview')
    )

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        return field_name in ('displayed')


class CreateEventClassForm(BaseEventClassForm):
    """
    Class representing event class create form.
    """
    name = wtforms.StringField(
        lazy_gettext('Name:'),
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=3, max=250),
            hawat.forms.check_null_character,
            hawat.forms.check_unique_event_class
        ]
    )


class UpdateEventClassForm(BaseEventClassForm):
    """
    Class representing event class update form.
    """
    name = wtforms.StringField(
        lazy_gettext('Name:'),
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=3, max=250),
            hawat.forms.check_null_character,
            check_event_class_name_uniqueness
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Store the ID of original item in database to enable the ID uniqueness
        # check with check_event_class_name_uniqueness() validator.
        self.db_item_id = kwargs['obj'].id


class EventClassSearchForm(hawat.forms.BaseSearchForm):
    """
    Class representing simple event class search form.
    """
    search = wtforms.StringField(
        lazy_gettext('Name, rule, label:'),
        validators=[
            wtforms.validators.Optional(),
            wtforms.validators.Length(min=3, max=100),
            hawat.forms.check_null_character
        ],
        filters=[
            lambda x: x or '',
            str.strip
        ],
        description=lazy_gettext(
            'Event class` name, content or label. Search is performed even in the middle of the strings.')
    )
    dt_from = hawat.forms.SmartDateTimeField(
        lazy_gettext('Creation time from:'),
        validators=[
            wtforms.validators.Optional()
        ],
        description=lazy_gettext(
            'Lower time boundary for item creation time. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences.')
    )
    dt_to = hawat.forms.SmartDateTimeField(
        lazy_gettext('Creation time to:'),
        validators=[
            wtforms.validators.Optional()
        ],
        description=lazy_gettext(
            'Upper time boundary for item creation time. Timestamp is expected to be in the format <code>YYYY-MM-DD hh:mm:ss</code> and in the timezone according to the user`s preferences.')
    )

    severity = wtforms.SelectField(
        lazy_gettext('Severity:'),
        validators=[
            wtforms.validators.Optional(),
        ],
        choices=[('', lazy_gettext('Nothing selected'))] + [(severity, severity) for severity in mentat.const.REPORT_SEVERITIES ],
        default='',
        description=lazy_gettext('Search for event classes of particular severity.')
    )
    type = wtforms.SelectField(
        lazy_gettext('Type:'),
        choices=[
            ('', lazy_gettext('Nothing selected')),
            ('source-based', lazy_gettext('Source-based')),
            ('target-based', lazy_gettext('Target-based'))
        ],
        default='',
        description=lazy_gettext('Search for event classes of the chosen type.')
    )
    state = wtforms.SelectField(
        lazy_gettext('State:'),
        validators=[
            wtforms.validators.Optional(),
        ],
        choices=[
            ('', lazy_gettext('Nothing selected')),
            ('enabled', lazy_gettext('Enabled')),
            ('disabled', lazy_gettext('Disabled'))
        ],
        default='',
        description=lazy_gettext('Search for event classes with particular state.')
    )

    sortby = wtforms.SelectField(
        lazy_gettext('Sort by:'),
        validators=[
            wtforms.validators.Optional()
        ],
        choices=[
            ('createtime.desc', lazy_gettext('by creation time descending')),
            ('createtime.asc', lazy_gettext('by creation time ascending')),
            ('name.desc', lazy_gettext('by name descending')),
            ('name.asc', lazy_gettext('by name ascending')),
        ],
        default='name.asc'
    )

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        return False
