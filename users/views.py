from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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


        
class Login(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        return reverse("user-home", kwargs={"username": self.request.user.username})

@login_required
def user_home(request, username):
    return render(request, 'pages/home.html', {'username': username})