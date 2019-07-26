from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserForm, ProfileForm, RoleFormSet
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def home(request):
     return render(request, 'home.html')

@login_required
def users_profile(request):
    if request.method == 'POST':
        profile_form = RoleFormSet(data=request.POST)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('home')

    else:
        profiles = Profile.objects.all()
        formset = RoleFormSet(queryset=profiles)
        profiles_and_formset = zip(profiles,formset)

    return render(request, 'users_profile.html', {'formset':formset, 'profiles': profiles})


# @method_decorator(login_required, name='dispatch')
# class UserUpdateView(UpdateView):
#     model = User
#     fields = ('first_name', 'last_name', 'email',)
#     template_name = 'my_account.html'
#     success_url = reverse_lazy('my_account')

#     def get_object(self):
#         return self.request.user


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'my_account.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
