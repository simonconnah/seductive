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
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from . import models


class BlogPostAdmin(GuardedModelAdmin):
    pass


class BlogCategoryAdmin(GuardedModelAdmin):
    pass


class BlogTagAdmin(GuardedModelAdmin):
    pass


class BlogPageAdmin(GuardedModelAdmin):
    pass


class BlogCommentAdmin(GuardedModelAdmin):
    pass


admin.site.register(models.BlogPost, BlogPostAdmin)
admin.site.register(models.BlogCategory, BlogCategoryAdmin)
admin.site.register(models.BlogTag, BlogTagAdmin)
admin.site.register(models.BlogPage, BlogPageAdmin)
admin.site.register(models.BlogComment, BlogCommentAdmin)
