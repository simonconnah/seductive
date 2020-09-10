'''
    seductiveblog - an open source blogging platform
    Copyright (C) 2018, Simon Connah

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django import forms
from django_registration.forms import RegistrationForm
from . import models


class SeductiveBlogRegistrationForm(RegistrationForm):
    username = forms.CharField(label=_('Username'))
    email = forms.EmailField(label=_('Email'))
    password1 = forms.CharField(label=_('Password'))
    password2 = forms.CharField(label=_('Confirm Password'))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.Form):
    website = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    website_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserProfileUpdateWebsiteForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['website', 'website_name']
        widgets = {
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'website_name': forms.TextInput(attrs={'class': 'form-control'})
        }
