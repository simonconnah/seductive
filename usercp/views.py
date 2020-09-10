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
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django_registration.backends.activation.views import RegistrationView, ActivationView
from .forms import SeductiveBlogRegistrationForm, UserProfileForm, UserProfileUpdateWebsiteForm
from .models import UserProfile


@login_required
@require_http_methods(['GET'])
def usercp_home(request):
    return render(request, 'usercp/home.html')


@login_required
@require_http_methods(['GET', 'POST'])
def usercp_profile(request, pk):
    current_site = get_current_site(request)
    form = UserProfileForm()
    try:
        user_profile = UserProfile.objects.get()
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, website=None, website_name=None)
        user_profile.save()
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.website = form.cleaned_data['website']
            user_profile.website_name = form.cleaned_data['website_name']
            user_profile.save()
            if user_profile.website is not None:
                context = {'user_profile': user_profile, 'user': request.user, 'form': form,
                           'site_name': current_site.name}
            else:
                context = {'user': request.user, 'form': form, 'site_name': current_site.name}
            return render(request, 'usercp/profile.html', context=context)
    if user_profile.website is not None:
        context = {'user_profile': user_profile, 'user': request.user, 'form': form, 'site_name': current_site.name}
    else:
        context = {'user': request.user, 'form': form, 'site_name': current_site.name}
    return render(request, 'usercp/profile.html', context=context)


class UserCPUpdateWebsiteDetails(UpdateView):
    model = UserProfile
    template_name = 'usercp/update_website.html'
    form_class = UserProfileUpdateWebsiteForm


class SeductiveBlogRegistrationView(RegistrationView):
    form_class = SeductiveBlogRegistrationForm

    def get_email_context(self, user):
        context = super().get_email_context(user)
        context['site_name'] = get_current_site(self.request).name
        return context


class SeductiveBlogActivationView(ActivationView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['site_name'] = get_current_site(self.request).name
        return context


# TODO: Pass in the correct context data to the Django Registration templates (email and normal)
# TODO: Replace Django Registration views with the new sub-classes
