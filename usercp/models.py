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
from django.contrib.auth.models import Permission
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

user = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE)
    num_blog_comments = models.PositiveIntegerField(default=0)
    num_blog_posts = models.PositiveIntegerField(default=0)
    num_images_uploaded = models.PositiveIntegerField(default=0)
    website = models.URLField(blank=True, null=True)
    website_name = models.TextField(blank=True, null=True)
    # the storage size is specified in megabytes
    max_image_storage_size = models.PositiveIntegerField(default=100)

    class Meta:
        permissions = (
            ('can_access_control_panel', _('Can access the control panel')),
        )


user_signal_model = get_user_model()


@receiver(post_save, sender=user_signal_model)
def usercp_comment_permissions_post_save(sender, **kwargs):
    if kwargs['instance'].username is not 'AnonymousUser':
        permission = Permission.objects.get(name='Can add Blog Comment')
        kwargs['instance'].user_permissions.add(permission)
