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
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from images.models import Image


class BlogPost(models.Model):
    title = models.TextField(verbose_name=_('Blog Title'))
    slug = models.SlugField()
    category = models.ForeignKey('BlogCategory', on_delete=models.CASCADE, verbose_name=_('The Category for the Post'),
                                 blank=True, null=True)
    tags = models.ManyToManyField('BlogTag', verbose_name=_('Tags Associated with the Post'), blank=True)
    # the short description is designed to be a shorter version of the blog post if the owner does not want to display
    # the full post on the front page - works well when a front page image is also specified
    short_content = models.TextField(verbose_name=_('Blog Extract'))
    long_content = models.TextField(verbose_name=_('Blog Post'))
    meta_description = models.TextField(verbose_name=_('Meta Description'))
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Posted'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date Updated'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Author'))
    front_page_image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name=_('Front Page Image'),
                                         blank=True, null=True)
    num_comments = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_article_detail', args=[str(self.id), self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('Blog Posts')
        verbose_name = _('Blog Post')
        get_latest_by = 'date_posted'


class BlogCategory(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name=_('The creator of the category'))
    name = models.TextField(verbose_name=_('Category Name'), unique=True)
    slug = models.SlugField()
    description = models.TextField(verbose_name=_('Category Description'), blank=True)
    meta_description = models.TextField(verbose_name=_('Meta Description'), blank=True)
    use_no_follow = models.BooleanField(default=True, verbose_name=_('Whether to make the Category no follow'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_category_detail', args=[str(self.id), self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Blog Categories')
        verbose_name = _('Blog Category')


class BlogTag(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name=_('The creator of the tag'))
    name = models.TextField(verbose_name=_('Tag Name'), unique=True)
    slug = models.SlugField()
    description = models.TextField(verbose_name=_('Tag Description'), blank=True)
    meta_description = models.TextField(verbose_name=_('Meta Description'), blank=True)
    use_no_follow = models.BooleanField(default=True, verbose_name=_('Whether to make the Tag no follow'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_tag_detail', args=[str(self.id), self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Blog Tags')
        verbose_name = _('Blog Tag')


class BlogPage(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Author of the page'))
    title = models.TextField(verbose_name=_('Title of the page'), unique=True)
    slug = models.SlugField()
    content = models.TextField(verbose_name=_('Page content'))
    meta_description = models.TextField(verbose_name=_('Meta Description'), blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_page_detail', args=[str(self.id), self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('Blog Pages')
        verbose_name = _('Blog Page')


class BlogComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name=_('Author of the comment'), blank=True, null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE,
                                       verbose_name=_('The parent comment to the current one'), null=True, blank=True)
    title = models.TextField(verbose_name=_('Title of the comment'))
    slug = models.SlugField()
    content = models.TextField(verbose_name=_('The comment'))
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name=_('Date comment posted'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date comment updated'))
    positive_votes = models.PositiveIntegerField(default=0)
    negative_votes = models.PositiveIntegerField(default=0)
    flagged_for_review = models.BooleanField(default=False)
    article_commented_on = models.ForeignKey('BlogPost', verbose_name=_('The article the comment is about'),
                                             on_delete=models.CASCADE)
    users_who_like_comment = ArrayField(models.TextField(), null=True, blank=True)
    users_who_dislike_comment = ArrayField(models.TextField(), null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_comment_detail', args=[str(self.id), self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('Blog Comments')
        verbose_name = _('Blog Comment')

# Django signals for blog app models


@receiver(pre_save, sender=BlogPost)
def blog_post_pre_save_perm_check(sender, **kwargs):
    user_model = get_user_model()
    author_user = get_object_or_404(user_model, pk=kwargs['instance'].author.id)
    if not author_user.has_perm('blog.add_blogpost'):
        # the user is not allowed to make blog posts
        raise PermissionDenied
    elif not author_user.has_perm('blog.change_blogpost') and kwargs['instance'].id:
        # the user is not allowed to change a blog post that already exists
        raise PermissionDenied


@receiver(post_save, sender=BlogPost)
def blog_post_post_save_assign_perms(sender, **kwargs):
    user_model = get_user_model()
    author_user = get_object_or_404(user_model, pk=kwargs['instance'].author.id)

    # assign permissions to the author of the blog post because they will need to maintain it in the future
    # this only assigns permissions to the author of the blog post itself - other users will be unable to edit
    # or delete it unless they are a superuser or have been given permission directly by someone else
    if not author_user.has_perm('blog.change_blogpost'):
        assign_perm('blog.change_blogpost', author_user, kwargs['instance'])
    if not author_user.has_perm('blog.delete_blogpost'):
        assign_perm('blog.delete_blogpost', author_user, kwargs['instance'])


@receiver(pre_save, sender=BlogComment)
def blog_comment_pre_save_perm_check(sender, **kwargs):
    user_model = get_user_model()
    if kwargs['instance'].author.id is not None:
        author_user = get_object_or_404(user_model, pk=kwargs['instance'].author.id)
        # TODO: We should make sure that all users have the add comment permission
        if not author_user.has_perm('blog.add_blogcomment'):
            raise PermissionDenied
        if not author_user.has_perm('blog.change_blogcomment'):
            raise PermissionDenied
    else:
        try:
            comment = BlogComment.objects.get(pk=kwargs['instance'].id)
        except BlogComment.DoesNotExist:
            return
        raise PermissionDenied


@receiver(pre_save, sender=BlogComment)
def blog_comment_post_save_author_cant_comment(sender, **kwargs):
    user_model = get_user_model()
    if kwargs['instance'].author.id is not None:
        author_user = get_object_or_404(user_model, pk=kwargs['instance'].author.id)
        if not BlogComment.objects.filter(users_who_like_comment__in=author_user.username):
            if kwargs['instance'].users_who_like_comment is None:
                kwargs['instance'].users_who_like_comment = [author_user.username]
            else:
                kwargs['instance'].users_who_like_comment.append(author_user.username)
        if not BlogComment.objects.filter(users_who_dislike_comment__in=author_user.username):
            if kwargs['instance'].users_who_dislike_comment is None:
                kwargs['instance'].users_who_dislike_comment = [author_user.username]
            else:
                kwargs['instance'].users_who_dislike_comment.append(author_user.username)

# TODO: Add permission checks for all other models
