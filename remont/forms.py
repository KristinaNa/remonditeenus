# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django.core.exceptions import ValidationError
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
        raise "skdkdkd"
        return super(TrimmedCharFormField, self).clean(value)


class AddForm(forms.Form):
    nimi = forms.CharField(label='nimi', max_length=25)
    mudel = forms.CharField(label='mudel', max_length=25)
    kirjeldus= forms.CharField(label='kirjeldus', max_length=25)
    tootja= forms.CharField(label='tootja', max_length=25)
    seriaalnumber= forms.CharField(label='seriaalnumber', max_length=25)

    def clean(self):
        form_data = self.cleaned_data
        for key in form_data:
            form_data[key]=form_data[key].strip()
            if len(form_data[key])==0:
                raise ValidationError(key+' ei koosneda tuhikutest')

        return form_data
            # if len(value.strip())==0:
            #     raise ValidationError('TÜHIK!!!')

    # def clean_nimi(self):
    #     nimi = self.cleaned_data['nimi']
    #     nimi = nimi.replace(' ', '') # remove all "a"s from message
    #     if len(nimi) < 1:
    #         raise ValidationError('Ei või koosneda tühikutest')
    #     return nimi
    #
    # def clean_nimi(self):
    #     nimi = self.cleaned_data['nimi']
    #     nimi = nimi.replace(' ', '') # remove all "a"s from message
    #     if len(nimi) < 1:
    #         raise ValidationError('Ei või koosneda tühikutest')
    #     return nimi

