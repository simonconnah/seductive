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
from django.db import models
from django.conf import settings


class ImageCategory(models.Model):
    name = models.TextField(verbose_name=_('Image Category Name'))
    description = models.TextField(verbose_name=_('Image Category Description'))
    meta_description = models.CharField(max_length=250, verbose_name=_('Image Category Meta Description'))

    class Meta:
        verbose_name_plural = _('Image Categories')
        verbose_name = _('Image')


class ImageTag(models.Model):
    name = models.TextField(verbose_name=_('Image Tag Name'))
    description = models.TextField(verbose_name=_('Image Tag Description'))
    meta_description = models.CharField(max_length=250, verbose_name=_('Image Tag Meta Description'))

    class Meta:
        verbose_name_plural = _('Image Tags')
        verbose_name = _('Image Tag')


class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name=_('Person who uploaded image'))
    name = models.TextField(verbose_name=_('Image Name'))
    description = models.TextField(verbose_name=_('Image Description'))
    meta_description = models.CharField(max_length=250, verbose_name=_('Image Meta Description'))
    alt_tag = models.CharField(max_length=300, verbose_name=_('Alt Tag Content for Image'))
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE, verbose_name=_('Image Category'))
    tags = models.ManyToManyField(ImageTag, blank=True, verbose_name=_('Image Tags'))
    image_height = models.PositiveIntegerField(verbose_name=_('Height of the Image'))
    image_width = models.PositiveIntegerField(verbose_name=_('Width of the Image'))
    image = models.ImageField(max_length=300, height_field=image_height, width_field=image_width,
                              verbose_name=_('Image'))

    class Meta:
        verbose_name_plural = _('Images')
        verbose_name = _('Image')
