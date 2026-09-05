import logging
from smtplib import SMTPException

from django.contrib import messages
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .emails import send_contact_email
from .forms import ContactForm


logger = logging.getLogger(__name__)


def HomePage(request):
    template = loader.get_template("pages/home.html")
    context = {}
    return HttpResponse(template.render(context, request))


def About(request):
    context = {}
    return render(request, "pages/about.html", context)


def Contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                send_contact_email(
                    name=form.cleaned_data["username"],
                    sender_email=form.cleaned_data["email"],
                    subject=form.cleaned_data["subject"],
                    message=form.cleaned_data["message"],
                )
            except (BadHeaderError, OSError, SMTPException):
                logger.exception("Contact email delivery failed")
                messages.error(
                    request,
                    "We could not send your message right now. Please try again later.",
                )
            else:
                return redirect("pages:thank-you")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})


def Thankyou(request):
    return render(request, "pages/thank_you.html")
