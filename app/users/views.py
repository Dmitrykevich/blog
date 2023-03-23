from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils.text import slugify
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Profile
from .forms import ProfileForm


class RegisterView(View):
    form_class = UserCreationForm
    template_name = 'users/registration.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            slug = slugify(user.username)
            Profile.objects.create(user=user, slug=slug)
            return redirect('main:index')
        context = {'form': form}
        return render(request, self.template_name, context)


class CustomLoginView(LoginView):
    next_page = 'main:index'
    template_name = 'users/login.html'


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'main:index'


class ProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'

    def get(self, request, slug):
        profile = Profile.objects.get(slug=slug)
        form = ProfileForm(instance=profile)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, slug):
        profile = Profile.objects.get(slug=slug)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Saved')
            return redirect(reverse_lazy('users:profile', kwargs={'slug': slug}))
        context = {'form': form}
        return render(request, self.template_name, context)
