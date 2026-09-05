from .models import Profile


def academic_profile(request):
    return {"site_profile": Profile.objects.first()}
