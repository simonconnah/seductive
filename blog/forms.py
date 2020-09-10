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

from django import forms
from . import models


class BlogPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(required=False, queryset=models.BlogCategory.objects.all())

    class Meta:
        model = models.BlogPost
        fields = ['title', 'short_content', 'long_content', 'meta_description', 'front_page_image', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_content': forms.Textarea(attrs={'class': 'form-control'}),
            'long_content': forms.Textarea(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control'}),
            'front_page_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = models.BlogCategory
        fields = ['name', 'description', 'meta_description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form_control'}),
        }


class BlogTagForm(forms.ModelForm):
    class Meta:
        model = models.BlogTag
        fields = ['name', 'description', 'meta_description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form_control'}),
        }


class BlogPageForm(forms.ModelForm):
    class Meta:
        model = models.BlogPage
        fields = ['title', 'content', 'meta_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form_control'}),
        }


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = models.BlogComment
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
