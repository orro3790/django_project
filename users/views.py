from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from classifieds.models import Ad, Job
from . models import (
    Profile
)
from django.utils.translation import gettext_lazy as _
from django.utils import translation


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _(f'Your account has been created! You are now able to login!'))
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
    
@login_required
def profile(request):
    # fetch all ads belonging to the user
    ads = Ad.objects.all()
    job_ads = Job.objects.all()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            if request.user.profile.language == 'English':
                translation.activate('en')
            if request.user.profile.language == 'Russian':
                translation.activate('ru')
            messages.success(request, _(f'Your account has been updated!'))
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'ads': ads,
        'job_ads': job_ads
    }
    return render(request, 'users/profile.html', context)


