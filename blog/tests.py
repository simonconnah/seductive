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
from django.test import TestCase, LiveServerTestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.sites.models import Site
from guardian.shortcuts import assign_perm, remove_perm
from selenium import webdriver
from .models import BlogPost, BlogCategory, BlogComment, BlogPage, BlogTag


class BlogPostTest(TestCase):
    fixtures = ['blog_user', 'blog_article', 'blog_category', 'blog_comment']

    # TODO: Change all of these unit tests to use fixtures instead of hardcoded items

    def setUp(self):
        self.user_model = get_user_model()
        self.superuser = self.user_model.objects.create_superuser(username='test_superuser', password='1234',
                                                                  email='super@user.com')
        self.test_blog_category = BlogCategory.objects.create(owner=self.superuser, name='Test Category')

        self.blog_post = BlogPost.objects.create(title='Superuser Blog Post', category=self.test_blog_category,
                                                 long_content='Very long content', author=self.superuser,
                                                 short_content='Very short content', meta_description='Meta')
        self.blog_post.save()

        self.fixtures = ['blog']

    def tearDown(self):
        self.superuser.delete()
        self.test_blog_category.delete()
        self.blog_post.delete()

    def test_superuser_can_create_blog_post(self):
        self.assertTrue(self.superuser.has_perm('blog.add_blogpost'))

    def test_superuser_can_update_blog_post(self):
        self.assertTrue(self.superuser.has_perm('blog.change_blogpost'))

    def test_superuser_can_delete_blog_post(self):
        self.assertTrue(self.superuser.has_perm('blog.delete_blogpost'))

    def test_normal_user_can_not_create_blog_post(self):
        user_model = get_user_model()

        test_create_user = user_model.objects.create(username='test_create', email='create@blah.com', password='1234')

        self.assertFalse(test_create_user.has_perm('blog.add_blogpost'))

        test_create_user.delete()

    def test_normal_user_can_not_update_blog_post(self):
        user_model = get_user_model()

        test_update_user = user_model.objects.create(username='test_update', email='update@blah.com', password='1234')

        self.assertFalse(test_update_user.has_perm('blog.change_blogpost', self.blog_post))

        test_update_user.delete()

    def test_normal_user_can_not_delete_blog_post(self):
        user_model = get_user_model()

        test_delete_user = user_model.objects.create(username='test_delete', email='blah@blah.com', password='1234')

        self.assertFalse(test_delete_user.has_perm('blog.delete_blogpost', self.blog_post))

        test_delete_user.delete()

    def test_single_user_perms_can_create_others_cant(self):
        user_model = get_user_model()

        can_create_user = user_model.objects.create(username='can_create', email='create@blah.com', password='1234')
        can_not_create_user = user_model.objects.create(username='can_not_create', email='not_create@blah.com',
                                                        password='1234')

        assign_perm('blog.add_blogpost', can_create_user)

        self.assertFalse(can_not_create_user.has_perm('blog.add_blogpost'))

        try:
            create_blog_post = BlogPost.objects.create(title='Temp blog post', author=can_create_user,
                                                       category=self.test_blog_category, long_content='long',
                                                       short_content='short', meta_description='meta')
        except PermissionDenied:
            self.fail('User can not create blog post when they should be able to.')

        with self.assertRaises(PermissionDenied):
            dont_create_blog_post = BlogPost.objects.create(title='Fail blog', author=can_not_create_user,
                                                            category=self.test_blog_category, long_content='long',
                                                            short_content='short', meta_description='meta')

        create_blog_post.delete()

        # we run this test because the blog wasn't created (PermissionDenied) above so trying to delete it should raise
        # an UnboundLocalError as the variable does not exist
        with self.assertRaises(UnboundLocalError):
            dont_create_blog_post.delete()

        can_create_user.delete()
        can_not_create_user.delete()

    def test_all_users_have_create_comment_permissions(self):
        pass

    def test_single_user_perms_can_update_others_cant(self):
        pass

    def test_single_user_perms_can_delete_others_cant(self):
        pass

    def test_default_user_group_can_create_posts(self):
        pass

    def test_default_user_group_can_update_posts(self):
        pass

    def test_default_user_group_can_delete_posts(self):
        pass

    def test_adding_user_to_group(self):
        pass

    def test_removing_user_from_group(self):
        pass


class BlogPostSeleniumTest(LiveServerTestCase):
    # TODO: Update the date and times in the fixtures to be unique so we can test that as well
    fixtures = ['blog_user', 'blog_article', 'blog_category', 'blog_comment']

    def setUp(self):
        self.firefox = webdriver.Firefox()

    def tearDown(self):
        self.firefox.close()

    def test_assert_user_can_login(self):
        pass

    def test_assert_user_can_logout(self):
        pass

    def test_assert_blog_post_on_homepage_firefox(self):
        self.firefox.get('http://localhost:8000')

        content = self.firefox.find_elements_by_class_name('blog-article')
        for article_title in content:
            if article_title.text == 'Test Post 1' or 'Test Post 2' or 'Test Post 3' or 'Test Post 4':
                self.assertTrue(True)
            else:
                self.fail('Unknown blog post title')

    def test_assert_blog_detail_page_firefox(self):
        self.firefox.get('http://localhost:8000/blog/article/1/test-post-1/')

        self.assertEqual(self.firefox.title, 'Test Post 1')

        main_text = self.firefox.find_element_by_id('main-content')

        self.assertEqual(main_text.text, 'This is the long content for the blog post Test Post 1. It should contain more data than the short_content.')

    def test_assert_comments_displayed_on_article_detail_page_firefox(self):
        self.firefox.get('http://localhost:8000/blog/article/1/test-post-1/')

        comment_titles = self.firefox.find_elements_by_class_name('comment-title')

        for comment_title in comment_titles:
            if comment_title.text == 'First Comment' or 'Test Comment' or 'Test Comment Again':
                self.assertTrue(True)
            else:
                self.fail('Comment not found in the database')

    def test_assert_comment_detail_page_firefox(self):
        self.firefox.get('http://localhost:8000/blog/comment/1/')

        comment_title = self.firefox.find_element_by_id('comment-title')

        self.assertEqual(comment_title.text, 'First Comment')

    def test_assert_comment_like_on_comment_detail_page_not_logged_in_firefox(self):
        self.firefox.get('http://localhost:8000/blog/comment/1/')

        if self.firefox.title != 'First Comment':
            self.fail('Wrong comment title on comment detail page')

        like_comment_button = self.firefox.find_element_by_id('like-comment-button')

        like_comment_button.click()

        if self.firefox.title != 'Login to example.com':
            self.fail('Did not redirect to login view when like comment button clicked')


class BlogCategoryTest(TestCase):
    pass


class BlogTagTest(TestCase):
    pass


class BlogPageTest(TestCase):
    pass


class BlogCommentTest(TestCase):
    pass
