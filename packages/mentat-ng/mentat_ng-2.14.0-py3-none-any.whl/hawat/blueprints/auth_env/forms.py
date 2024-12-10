#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
# -------------------------------------------------------------------------------


"""
This module contains custom user account registration form for Hawat.
"""

__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

from flask_babel import lazy_gettext
import wtforms

from hawat.blueprints.users.forms import BaseUserAccountForm
import hawat.forms


class RegisterUserAccountForm(BaseUserAccountForm):
    """
    Class representing user account registration form.
    """
    memberships_wanted = wtforms.SelectMultipleField(
        lazy_gettext('Requested group memberships:'),
        default=[],
        coerce=hawat.forms.coerce_group,
        filters=[hawat.forms.filter_none_from_list]
    )
    justification = wtforms.TextAreaField(
        lazy_gettext('Justification:'),
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=10, max=500)
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        groups = hawat.forms.get_available_groups()
        self.memberships_wanted.choices = [(group, group.name) for group in groups]
