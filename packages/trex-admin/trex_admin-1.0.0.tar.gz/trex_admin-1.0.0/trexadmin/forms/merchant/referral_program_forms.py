'''
Created on 9 Apr 2024

@author: jacklok
'''

from wtforms import StringField, PasswordField, validators, BooleanField, SelectField, SelectMultipleField, IntegerField
from wtforms.fields.html5 import DateField
from trexadmin.forms.base_forms import ValidationBaseForm
from trexadmin.libs.wtforms import validators as custom_validator
from trexadmin.forms.common.common_forms import CheckBoxField, CustomDateField,\
    CustomIntegerField
from datetime import date
from wtforms.fields.core import FloatField
from flask_babel import gettext
from trexmodel import program_conf
from trexadmin.libs.wtforms import fields as custom_fields
from trexadmin.libs.wtforms.fields import IgnoreChoiceSelectMultipleField,\
    IgnoreChoiceSelectField, JSONField, CurrencyField
from wtforms.validators import Length
from wtforms.fields.simple import HiddenField

class ProgramBaseForm(ValidationBaseForm):
    
    program_key             = HiddenField('Program Key')

class ReferralProgramDetailsForm(ProgramBaseForm):
    label                    = StringField('Label', [
                                        validators.InputRequired(gettext('Program Label is required')),
                                        Length(max=100)
                                        ]
                                        )
    start_date              = DateField('Program Start Date', default=date.today, format='%d/%m/%Y')
    end_date                = DateField('Program End Date', default=date.today, format='%d/%m/%Y')
    desc                    = StringField('Description', [
                                        ]
                                        )
    
class ReferralProgramPromoteTextForm(ValidationBaseForm):
    promote_title           = StringField('Promote Title', [
                                        validators.InputRequired(gettext('Promote title is required')),
                                        Length(max=500)
                                        ]
                                        )
    promote_desc           = StringField('Promote Description', [
                                        validators.InputRequired(gettext('Promote Description is required')),
                                        Length(max=3000)
                                        ]
                                        )
    