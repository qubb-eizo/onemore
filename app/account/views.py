from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from account.forms import UserAccountRegistrationForm, UserAccountProfileForm
from app import settings


class CreateUserAccountView(CreateView):
    model = settings.AUTH_USER_MODEL
    template_name = 'registration.html'
    form_class = UserAccountRegistrationForm

    def get_success_url(self):
        messages.success(self.request, "New user has been successfully created!")
        return reverse('profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Register new user'
        return context


class UserAccountLoginView(LoginView):
    template_name = 'login.html'
    extra_context = {'title': 'Login as a user'}

    def get_success_url(self):
        messages.success(self.request, "You've just successfully logged in")
        return reverse('account:profile')


class UserAccountLogoutView(LogoutView):
    template_name = 'logout.html'
    extra_context = {'title': 'Logout from LMS'}


class UserAccountUpdateView(UpdateView):
    template_name = 'profile.html'
    extra_context = {'title': 'Edit current user profile'}
    form_class = UserAccountProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('index')
