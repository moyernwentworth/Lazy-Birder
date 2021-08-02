from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    """logic behind logging in or registering an account"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # saves a user to the db and hashes password automatically
            form.save()
            # stores username created for messaging
            username = form.cleaned_data.get('username')
            # displays success with username
            messages.success(request, f'{username}, your account has been created! You can now log in.')
            # logs user in and sends them to home page
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# decorator which ensures user is logged in
@login_required
def profile(request):
    """send users to their specific profile, ensuring theyre logged in"""
    # These populate the associated forms with the logged in users' info
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        # if all info is updated properly, the user and profile objects are updated
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # render function below takes in a dict of content to be displayed
    # in this case is is the user's info
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    # returns the updated page to be viewed
    return render(request, 'users/profile.html', context)
