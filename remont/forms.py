# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django.utils.translation import gettext_lazy as _
from django import forms

# class UserCreationForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserCreationForm, self).__init__(*args, **kwargs)
#
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             'username',
#             'password1',
#             'password2',
#             ButtonHolder(
#                 Submit('register', 'Register', css_class='btn-primary')
#             )
#         )
#
#
# class AuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(AuthenticationForm, self).__init__(*args, **kwargs)
#
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             'username',
#             'password',
#             ButtonHolder(
#                 Submit('login', 'Login', css_class='btn-primary')
#             )
#         )

class TrimmedCharFormField(forms.CharField):
    def clean(self, value):
        if value:
            value = value.strip()
        return super(TrimmedCharFormField, self).clean(value)


class AddForm(forms.Form):
    nimi = forms.CharField(label='nimi', max_length=25)
    mudel = forms.CharField(label='mudel', max_length=25)
    kirjeldus= forms.CharField(label='kirjeldus', max_length=25)
    tootja= forms.CharField(label='tootja', max_length=25)
    seriaalnumber= forms.CharField(label='seriaalnumber', max_length=25)
    def clean(self):
        cleaned_data = super(AddForm, self).clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject:
            # Only do something if both fields are valid so far.
            if "help" not in subject:
                raise forms.ValidationError(
                    "Did not send for 'help' in the subject despite "
                    "CC'ing yourself."
                )