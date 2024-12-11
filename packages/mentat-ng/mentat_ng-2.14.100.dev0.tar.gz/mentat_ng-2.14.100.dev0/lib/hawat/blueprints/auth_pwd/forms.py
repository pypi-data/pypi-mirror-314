#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
# -------------------------------------------------------------------------------


"""
This module contains custom developer login form for Hawat.
"""

__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

from flask_babel import lazy_gettext
import flask_wtf
import wtforms

from hawat.blueprints.users.forms import BaseUserAccountForm
import hawat.forms
from hawat.forms import check_login, check_null_character, check_unique_login


class LoginForm(flask_wtf.FlaskForm):
    """
    Class representing classical password authentication login form.
    """
    login = wtforms.StringField(
        lazy_gettext('Login:'),
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=3, max=50),
            check_null_character,
            check_login
        ]
    )
    password = wtforms.PasswordField(
        lazy_gettext('Password:'),
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=8),
        ]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Login')
    )


class RegisterUserAccountForm(BaseUserAccountForm):
    """
    Class representing classical account registration form.
    """
    login = wtforms.StringField(
        lazy_gettext('Login:'),
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=3, max=50),
            check_null_character,
            check_login,
            check_unique_login
        ]
    )
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
    password = wtforms.PasswordField(
        lazy_gettext('Password:'),
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=8),
        ]
    )
    password2 = wtforms.PasswordField(
        lazy_gettext('Repeat Password:'),
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo('password'),
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        groups = hawat.forms.get_available_groups()
        self.memberships_wanted.choices = [(group, group.name) for group in groups]
