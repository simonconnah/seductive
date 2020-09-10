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
from django.core import serializers
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic import TemplateView, ListView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from usercp.models import UserProfile
from .models import BlogPost, BlogCategory, BlogTag, BlogPage, BlogComment
from . import forms


class HomeView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class ContactUsView(TemplateView):
    template_name = 'blog/contact_us.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'blog/privacy_policy.html'


class TermsOfServiceView(TemplateView):
    template_name = 'blog/terms_of_service.html'


class ControlPanelHome(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'usercp.can_access_control_panel'
    permission_denied_message = _('You do not have permission to access the control panel')
    template_name = 'blog/cp/home.html'


class ControlPanelBlogPostHome(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/cp/article_home.html'
    permission_required = 'usercp.can_access_control_panel'
    permission_denied_message = _('You do not have permission to access the control panel')


class ControlPanelBlogCategoryHome(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BlogCategory
    template_name = 'blog/cp/category_home.html'
    permission_required = 'usercp.can_access_control_panel'
    permission_denied_message = _('You do not have permission to access the control panel')


class ControlPanelBlogPageHome(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BlogPage
    template_name = 'blog/cp/page_home.html'
    permission_required = 'usercp.can_access_control_panel'
    permission_denied_message = _('You do not have permission to access the control panel')


class ControlPanelBlogTagHome(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BlogTag
    template_name = 'blog/cp/tag_home.html'
    permission_required = 'usercp.can_access_control_panel'
    permission_denied_message = _('You do not have permission to access the control panel')


class ControlPanelBlogCommentHome(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BlogComment
    template_name = 'blog/cp/comment_home.html'
    permission_required = 'usercp.can_access_control_panel'
    permission_denied_message = _('You do not have permission to access the control panel')


class ControlPanelBlogCommentListByArticle(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BlogComment
    template_name = 'blog/cp/comment_list_by_article.html'
    permission_required = 'usercp.can_access_control_panel'
    permission_denied_message = _('You do not have permission to access the control panel')

    def get_queryset(self):
        return BlogComment.objects.filter(article_commented_on=self.kwargs['article_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = get_object_or_404(BlogPost, pk=self.kwargs['article_id'])
        return context


class ControlPanelBlogCommentListReported(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BlogComment
    template_name = 'blog/cp/comment_list_reported_comments.html'
    permission_required = 'usercp_can_access_control_panel'
    permission_denied_message = _('You do not have permission to access the control panel')

    def get_queryset(self):
        return BlogComment.objects.filter(flagged_for_review=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = get_current_site(self.request).name
        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        context['comments'] = BlogComment.objects.filter(article_commented_on=self.object)
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPost
    form_class = forms.BlogPostForm
    slug_field = ['slug']
    template_name = 'blog/cp/article_update_form.html'
    permission_required = 'blog.change_blogpost'
    permission_denied_message = _('You do not have permission to change blog posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        context['comments'] = BlogComment.objects.filter(article_commented_on=self.object)
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('home')
    template_name = 'blog/cp/article_delete_form.html'
    permission_required = 'blog.delete_blogpost'
    permission_denied_message = _('You do not have permission to delete blog posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context

    def get_success_url(self):
        return reverse_lazy('blog_article_control_panel_home')


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/article_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/cp/article_create_form.html'
    form_class = forms.BlogPostForm
    permission_required = 'blog.add_blogpost'
    permission_denied_message = _('You do not have permission to create blog posts')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context

    def get_success_url(self):
        return reverse_lazy('blog_article_detail', kwargs={
            'pk': str(self.object.id),
            'article_slug': self.object.slug
        })


class BlogCategoryDetailView(DetailView):
    model = BlogCategory
    template_name = 'blog/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        context['articles'] = BlogPost.objects.filter(category=self.object)
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogCategoryListView(ListView):
    model = BlogCategory
    template_name = 'blog/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogCategory
    template_name = 'blog/cp/category_create_form.html'
    form_class = forms.BlogCategoryForm
    permission_required = 'blog.add_blogcategory'
    permission_denied_message = _('You do not have permission to create a blog category')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.owner = self.request.user
        f.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context

    def get_success_url(self):
        return reverse_lazy('blog_category_detail', kwargs={
            'pk': str(self.object.id),
            'category_slug': self.object.slug
        })


class BlogCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogCategory
    success_url = reverse_lazy('home')
    template_name = 'blog/cp/category_delete_form.html'
    permission_required = 'blog.delete_blogcategory'
    permission_denied_message = _('You do not have permission to delete blog categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogCategory
    form_class = forms.BlogCategoryForm
    slug_field = ['slug']
    template_name = 'blog/cp/category_update_view.html'
    permission_required = 'blog.change_blogcategory'
    permission_denied_message = _('You do not have permission to change blog categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogTagDetailView(DetailView):
    model = BlogTag
    template_name = 'blog/tag_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        context['articles'] = BlogPost.objects.filter(tags__name__contains=self.object.name)
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogTagListView(ListView):
    model = BlogTag
    template_name = 'blog/tag_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogTagCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogTag
    template_name = 'blog/cp/tag_create_form.html'
    form_class = forms.BlogTagForm
    permission_required = 'blog.add_blogtag'
    permission_denied_message = _('You do not have permission to create blog tags')

    def form_valid(self, form):
        f = form.save(commit=False)
        if self.request.user.is_authenticated:
            f.owner = self.request.user
        else:
            f.owner = None
        f.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogTagDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogTag
    success_url = reverse_lazy('home')
    template_name = 'blog/cp/tag_delete_form.html'
    permission_required = 'blog.delete_blogtag'
    permission_denied_message = _('You do not have permission to delete blog tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogTagUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogTag
    form_class = forms.BlogTagForm
    slug_field = ['slug']
    template_name = 'blog/cp/tag_update_form.html'
    permission_required = 'blog_change_blogtag'
    permission_denied_message = _('You do not have permission to change blog tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogPageDetailView(DetailView):
    model = BlogPage
    template_name = 'blog/page_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogPageListView(ListView):
    model = BlogPage
    template_name = 'blog/page_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogPageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPage
    template_name = 'blog/cp/page_create_form.html'
    form_class = forms.BlogPageForm
    permission_required = 'blog_add_blogpage'
    permission_denied_message = _('You do not have permission to create blog pages')

    def form_valid(self, form):
        f = form.save(commit=False)
        if self.request.user.is_authenticated:
            f.author = self.request.user
        else:
            f.author = None
        f.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context

    def get_success_url(self):
        return reverse_lazy('blog_page_control_panel_home')


class BlogPageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPage
    success_url = reverse_lazy('home')
    template_name = 'blog/cp/page_delete_form.html'
    permission_required = 'blog.delete_blogpage'
    permission_denied_message = _('You do not have permission to delete blog pages')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogPageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPage
    form_class = forms.BlogPageForm
    slug_field = ['slug']
    template_name = 'blog/cp/page_update_form.html'
    permission_required = 'blog.change_blogpage'
    permission_denied_message = _('You do not have permission to change blog pages')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogCommentListView(ListView):
    model = BlogComment
    template_name = 'blog/comment_list.html'

    def get_queryset(self):
        return BlogComment.objects.filter(article_commented_on=self.kwargs['article_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['article'] = get_object_or_404(BlogPost, pk=self.kwargs['article_id'])
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogCommentDetailView(DetailView):
    model = BlogComment
    template_name = 'blog/comment_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


class BlogCommentCreateView(CreateView):
    model = BlogComment
    form_class = forms.BlogCommentForm
    template_name = 'blog/comment_create.html'

    def form_valid(self, form):
        self.blog_post = BlogPost.objects.get(pk=self.kwargs['article_id'])

        f = form.save(commit=False)
        if self.request.user.is_authenticated:
            f.author = self.request.user
        else:
            f.author = None
        f.article_commented_on = self.blog_post
        f.save()

        self.blog_post.num_comments += 1
        self.blog_post.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['article'] = BlogPost.objects.get(pk=self.kwargs['article_id'])
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context

    def get_success_url(self):
        return reverse_lazy('blog_article_detail', kwargs={
            'pk': str(self.kwargs['article_id']), 'article_slug': self.blog_post.slug
        })


class BlogCommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogComment
    success_url = reverse_lazy('home')
    template_name = 'blog/cp/comment_delete_form.html'
    permission_required = 'blog.delete_blogcomment'
    permission_denied_message = _('You do not have permission to delete blog comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context


# TODO: Make sure update view works
class BlogCommentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogComment
    form_class = forms.BlogCommentForm
    slug_field = ['slug']
    template_name = 'blog/cp/comment_update_form.html'
    permission_required = 'blog.change_blogcomment'
    permission_denied_message = _('You do not have permission to change blog comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['site_name'] = get_current_site(self.request).name
        if self.request.user.is_authenticated:
            try:
                context['user_profile'] = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                pass
        return context

    def get_success_url(self):
        return reverse_lazy('blog_comment_detail', kwargs={'pk': str(self.object.id)})


def blog_comment_like(request, comment_id):
    if request.user.is_authenticated:
        if not BlogComment.objects.filter(users_who_like_comment__contains=[request.user.username]):
            comment = BlogComment.objects.get(pk=comment_id)
            comment.positive_votes += 1
            if comment.users_who_like_comment is None:
                comment.users_who_like_comment = [request.user.username]
            else:
                comment.users_who_like_comment.append(request.user.username)
            comment.save()
            return HttpResponseRedirect(reverse_lazy('blog_comment_vote_success',
                                                     kwargs={'comment_id': str(comment_id)}))
        else:
            return HttpResponseRedirect(reverse_lazy('blog_comment_vote_fail', kwargs={'comment_id': str(comment_id)}))
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


def blog_comment_dislike(request, comment_id):
    if request.user.is_authenticated:
        if not BlogComment.objects.filter(users_who_dislike_comment__contains=[request.user.username]):
            comment = BlogComment.objects.get(pk=comment_id)
            comment.negative_votes += 1
            if comment.users_who_dislike_comment is None:
                comment.users_who_dislike_comment = [request.user.username]
            else:
                comment.users_who_dislike_comment.append(request.user.username)
            comment.save()
            return HttpResponseRedirect(reverse_lazy('blog_comment_vote_success',
                                                     kwargs={'comment_id': str(comment_id)}))
        else:
            return HttpResponseRedirect(reverse_lazy('blog_comment_vote_fail', kwargs={'comment_id': str(comment_id)}))
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


def blog_report_comment(request, comment_id):
    comment = BlogComment.objects.get(pk=comment_id)
    comment.flagged_for_review = True
    comment.save()
    return HttpResponseRedirect(reverse_lazy('blog_article_detail',
                                             kwargs={'pk': str(comment.article_commented_on.id),
                                                     'article_slug': comment.article_commented_on.slug}))


def blog_comment_vote_fail(request, comment_id):
    comment = BlogComment.objects.get(pk=comment_id)
    article = BlogPost.objects.get(pk=comment.article_commented_on.id)
    return TemplateResponse(request, 'blog/vote_fail.html', {'article': article, 'comment': comment})


def blog_comment_vote_success(request, comment_id):
    comment = BlogComment.objects.get(pk=comment_id)
    article = BlogPost.objects.get(pk=comment.article_commented_on.id)
    return TemplateResponse(request, 'blog/vote_success.html', {'article': article, 'comment': comment})
