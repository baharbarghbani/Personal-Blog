from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, your account has been created successfully!')
            return redirect('login')  
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


        
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Handle login logic here
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome back {username}!')
            return redirect('home')  # Redirect to home or another page after login
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})