from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
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


# decorator adds function to exisiting stuff
@login_required
def profile(request):
    """send users to their specific profile, ensuring theyre logged in"""
    return render(request, 'users/profile.html')

