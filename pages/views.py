from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def HomePage(request):
    template = loader.get_template('pages/home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def About(request):
    context={}
    return render(request, 'pages/about.html', context)

def Contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            subject = form.cleaned_data.get("subject")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")

            full_message = f"Message from {username}\n<{email}>:\n\n\n{message}"
            send_mail (
                subject, 
                full_message,
                settings.DEFAULT_FROM_EMAIL, # from
                [settings.CONTACT_RECEIVER_EMAIL] #to
            )
            return redirect("pages:thank-you")
    else:
            form = ContactForm()
    return render(request, 'pages/contact.html', {"form":form} )


def Thankyou(request):
    return render(request, "pages/thank_you.html")

