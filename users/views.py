from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

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

class Logout(LogoutView):
    next_page = "pages:home"

    def post(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().post(request, *args, **kwargs)

        
class Login(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm
