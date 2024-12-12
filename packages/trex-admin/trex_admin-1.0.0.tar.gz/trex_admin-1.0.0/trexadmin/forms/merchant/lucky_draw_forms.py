from wtforms import StringField, PasswordField, validators, BooleanField, SelectField, SelectMultipleField, IntegerField
from wtforms.fields.html5 import DateField
from trexadmin.forms.base_forms import ValidationBaseForm
from trexadmin.libs.wtforms import validators as custom_validator
from trexadmin.forms.common.common_forms import CheckBoxField, CustomDateField,\
    CustomIntegerField
from datetime import date
from wtforms.fields.simple import HiddenField
from flask_babel import gettext


class LuckyDrawSetupForm(ValidationBaseForm):
    lucky_draw_key             = HiddenField('Lucky Draw Key')
    

    label                      = StringField('Name of Draw', [
                                        validators.InputRequired(gettext('Name of Draw is required'))
                                        ]
                                        )    
