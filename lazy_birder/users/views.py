from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # saves a user to the db and hashes password automatically
            form.save()
            # stores username created for messaging
            username = form.cleaned_data.get('username')
            # displays success with username
            messages.success(request, f'Account created for {username}!')
            # logs user in and sends them to home page
            return redirect('dashbird-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
