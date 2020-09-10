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
from django.urls import path
from . import views

urlpatterns = [
    # general URLs
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms-of-service'),

    # general control panel URLs
    path('control-panel/', views.ControlPanelHome.as_view(), name='control_panel'),

    # user facing blog article URLs
    path('article/<int:pk>/<slug:article_slug>/', views.BlogPostDetailView.as_view(),
         name='blog_article_detail'),
    path('article/list/', views.BlogPostListView.as_view(), name='blog_article_list'),

    # blog article control panel URLs
    path('control-panel/articles/', views.ControlPanelBlogPostHome.as_view(), name='blog_article_control_panel_home'),
    path('control-panel/create-post/', views.BlogPostCreateView.as_view(), name='blog_article_create'),
    path('control-panel/update-post/<int:pk>/', views.BlogPostUpdateView.as_view(), name='blog_article_update'),
    path('control-panel/delete-post/<int:pk>/', views.BlogPostDeleteView.as_view(), name='blog_article_delete'),

    # user facing blog category URLs
    path('category/<int:pk>/<slug:category_slug>/', views.BlogCategoryDetailView.as_view(),
         name='blog_category_detail'),
    path('category/list/', views.BlogCategoryListView.as_view(), name='blog_category_list'),

    # blog category control panel URLs
    path('control-panel/categories/', views.ControlPanelBlogCategoryHome.as_view(),
         name='blog_category_control_panel_home'),
    path('control-panel/create-category/', views.BlogCategoryCreateView.as_view(), name='blog_category_create'),
    path('control-panel/update-category/<int:pk>/', views.BlogCategoryUpdateView.as_view(),
         name='blog_category_update'),
    path('control-panel/delete-category/<int:pk>/', views.BlogCategoryDeleteView.as_view(),
         name='blog_category_delete'),

    # user facing blog tag URLs
    path('tag/<int:pk>/<slug:tag_slug>/', views.BlogTagDetailView.as_view(), name='blog_tag_detail'),
    path('tag/list/', views.BlogTagListView.as_view(), name='blog_tag_list'),

    # blog tag control panel URLs
    path('control-panel/tags/', views.ControlPanelBlogTagHome.as_view(), name='blog_tag_control_panel_home'),
    path('control-panel/create-tag/', views.BlogTagCreateView.as_view(), name='blog_tag_create'),
    path('control-panel/update-tag/<int:pk>/', views.BlogTagUpdateView.as_view(), name='blog_tag_update'),
    path('control-panel/delete-tag/<int:pk>/', views.BlogTagDeleteView.as_view(), name='blog_tag_delete'),

    # user facing blog page URLs
    path('page/<int:pk>/<slug:page_slug>/', views.BlogPageDetailView.as_view(), name='blog_page_detail'),
    path('page/list/', views.BlogPageListView.as_view(), name='blog_page_list'),

    # blog page control panel URLs
    path('control-panel/pages/', views.ControlPanelBlogPageHome.as_view(), name='blog_page_control_panel_home'),
    path('control-panel/create-page/', views.BlogPageCreateView.as_view(), name='blog_page_create'),
    path('control-panel/update-page/<int:pk>/', views.BlogPageUpdateView.as_view(), name='blog_page_update'),
    path('control-panel/delete-page/<int:pk>/', views.BlogPageDeleteView.as_view(), name='blog_page_delete'),

    # blog comment control panel URLs
    path('control-panel/comments/', views.ControlPanelBlogCommentHome.as_view(),
         name='blog_comment_control_panel_home'),
    path('control-panel/comment/list/<int:article_id>/', views.ControlPanelBlogCommentListByArticle.as_view(),
         name='blog_comment_list_by_article_control_panel'),
    path('control-panel/comment/list/reported/', views.ControlPanelBlogCommentListReported.as_view(),
         name='blog_comment_list_reported_control_panel'),
    path('control-panel/delete-comment/<int:pk>/', views.BlogCommentDeleteView.as_view(), name='blog_comment_delete'),
    path('control-panel/update-comment/<int:pk>/', views.BlogCommentUpdateView.as_view(), name='blog_comment_update'),

    # user facing comment URLs
    path('comment/<int:pk>/', views.BlogCommentDetailView.as_view(), name='blog_comment_detail'),
    path('comment/list/<int:article_id>/', views.BlogCommentListView.as_view(), name='blog_comment_list_by_article'),
    path('comment/create-comment/<int:article_id>/', views.BlogCommentCreateView.as_view(), name='blog_comment_create'),

    # user facing comment voting URLs
    path('comment/like/<int:comment_id>/', views.blog_comment_like, name='blog_comment_like'),
    path('comment/dislike/<int:comment_id>/', views.blog_comment_dislike, name='blog_comment_dislike'),
    path('comment/report/<int:comment_id>/', views.blog_report_comment, name='blog_comment_report'),
    path('comment/<int:comment_id>/success/', views.blog_comment_vote_success, name='blog_comment_vote_success'),
    path('comment/<int:comment_id>/fail/', views.blog_comment_vote_fail, name='blog_comment_vote_fail'),
]
