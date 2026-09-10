import logging
from smtplib import SMTPException
from pathlib import Path

from django.contrib import messages
from django.core.mail import BadHeaderError
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .emails import send_contact_email
from .forms import ContactForm
from .models import Experience, Profile, Project, Research


logger = logging.getLogger(__name__)


def HomePage(request):
    visible_research = Research.objects.filter(is_visible=True)
    visible_projects = Project.objects.filter(is_visible=True)
    visible_experiences = Experience.objects.filter(is_visible=True)
    featured_research = visible_research.filter(featured=True)
    featured_projects = visible_projects.filter(featured=True)
    featured_experiences = visible_experiences.filter(featured=True)

    context = {
        "profile": Profile.objects.first(),
        "featured_research": (
            featured_research[:3] if featured_research.exists() else visible_research[:3]
        ),
        "featured_projects": (
            featured_projects[:3] if featured_projects.exists() else visible_projects[:3]
        ),
        "featured_experiences": (
            featured_experiences[:3]
            if featured_experiences.exists()
            else visible_experiences[:3]
        ),
    }
    return render(request, "pages/home.html", context)


def About(request):
    return render(
        request,
        "pages/about.html",
        {"profile": Profile.objects.first()},
    )


def research(request):
    research_items = Research.objects.filter(is_visible=True)
    return render(
        request,
        "pages/research.html",
        {"research_items": research_items},
    )


def research_detail(request, slug):
    research_item = get_object_or_404(Research, slug=slug, is_visible=True)
    return render(
        request,
        "pages/research_detail.html",
        {"research_item": research_item},
    )


def projects(request):
    project_items = Project.objects.filter(is_visible=True)
    return render(
        request,
        "pages/projects.html",
        {"project_items": project_items},
    )


def experience(request):
    experience_items = Experience.objects.filter(is_visible=True)
    return render(
        request,
        "pages/experience.html",
        {"experience_items": experience_items},
    )


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_visible=True)
    return render(
        request,
        "pages/project_detail.html",
        {"project": project},
    )


def download_cv(request):
    profile = Profile.objects.first()
    if profile and profile.cv:
        filename = Path(profile.cv.name).name
        return FileResponse(profile.cv.open("rb"), as_attachment=True, filename=filename)

    bundled_cv = (
        Path(__file__).resolve().parent
        / "static"
        / "documents"
        / "bahar-barghbani-cv.pdf"
    )
    if not bundled_cv.exists():
        raise Http404("A CV has not been uploaded yet.")

    return FileResponse(
        bundled_cv.open("rb"),
        as_attachment=True,
        filename="Bahar-Barghbani-CV.pdf",
    )


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
