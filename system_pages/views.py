from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render
from valutes.views import CurrencyArticleMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View, FormView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

class RegisterUser(CurrencyArticleMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('system_pages:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)



class LoginUser(CurrencyArticleMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


def logout_user(request):
    logout(request)
    return redirect('/')


class ProfileUser(LoginRequiredMixin, CurrencyArticleMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'profile.html'

    def get_success_url(self):
        return reverse_lazy('system_pages:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class UserPasswordChange(CurrencyArticleMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "password_change_form.html"
    success_url = reverse_lazy("system_pages:password_change_done")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class PasswordChangeDoneView(CurrencyArticleMixin, View):
    template_name = "password_change_form.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
