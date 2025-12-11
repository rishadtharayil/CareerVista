from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from careers.models import UserProgress

# ...

class ProfileWebView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progress_list'] = UserProgress.objects.filter(
            user=self.request.user
        ).select_related('roadmap_step', 'roadmap_step__roadmap', 'roadmap_step__roadmap__career')
        return context

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class ProfileWebView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add context for saved careers or progress
        return context
