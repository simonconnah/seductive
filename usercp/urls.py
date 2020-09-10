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
    path('', views.usercp_home, name='usercp_home'),
    path('profile/<int:pk>/', views.usercp_profile, name='usercp_profile'),
    path('profile/update-website/<int:pk>/', views.UserCPUpdateWebsiteDetails.as_view(), name='update_profile_website'),
    path('accounts/register/', views.SeductiveBlogRegistrationView.as_view(), name='usercp_registration'),
]
