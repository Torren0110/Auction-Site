from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request, 'New User Created')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/signup.html', context={'form':form})

def log_out(request):
    logout(request)

    messages.success(request, 'You have been logged out.')

    return redirect('home')
