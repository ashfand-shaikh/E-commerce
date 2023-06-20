from django.contrib.auth.views import LoginView, LogoutView
from django.db import models
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from users.forms import RegisterForm
from users.models import User


class RegisterView(View):
    def get(self, request):
        return render(request, "users/signup.html", {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse("login"))

        return render(request, "users/signup.html", {"form": form})


class LoginView(LoginView):
    template_name = "users/login.html"


class ProfileView(ListView):
    template_name = "users/profile.html"
    model = User 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.request.user
        return context
