from django.contrib import admin

from .models import Experience, Profile, Project, Research


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Introduction",
            {
                "fields": (
                    "full_name",
                    "professional_title",
                    "short_bio",
                )
            },
        ),
        (
            "Academic background",
            {
                "fields": (
                    "major",
                    "institution",
                    "education_details",
                    "research_interests",
                )
            },
        ),
        ("About", {"fields": ("about", "personal_note", "location")}),
        (
            "Qualifications",
            {"fields": ("awards", "technical_skills", "languages", "service")},
        ),
        (
            "Contact and profiles",
            {
                "fields": (
                    "email",
                    "github_url",
                    "linkedin_url",
                    "scholar_url",
                    "orcid_url",
                )
            },
        ),
        ("Curriculum vitae", {"fields": ("cv",)}),
    )

    def has_add_permission(self, request):
        return not Profile.objects.exists() and super().has_add_permission(request)


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "field",
        "year",
        "featured",
        "is_visible",
        "display_order",
    )
    list_editable = ("featured", "is_visible", "display_order")
    list_filter = ("status", "featured", "is_visible", "year")
    search_fields = ("title", "field", "summary", "abstract", "venue")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Overview", {"fields": ("title", "slug", "field", "summary", "abstract")}),
        (
            "Academic details",
            {"fields": ("status", "venue", "year", "collaborators")},
        ),
        ("Links", {"fields": ("publication_url", "code_url")}),
        (
            "Presentation",
            {"fields": ("featured", "is_visible", "display_order")},
        ),
        ("History", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date_label",
        "technologies",
        "featured",
        "is_visible",
        "display_order",
    )
    list_editable = ("featured", "is_visible", "display_order")
    list_filter = ("featured", "is_visible")
    search_fields = ("title", "summary", "description", "technologies")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Overview",
            {"fields": ("title", "slug", "date_label", "summary", "description")},
        ),
        ("Build", {"fields": ("technologies", "image")}),
        ("Links", {"fields": ("repository_url", "live_url")}),
        (
            "Presentation",
            {"fields": ("featured", "is_visible", "display_order")},
        ),
        ("History", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "role",
        "organization",
        "kind",
        "date_label",
        "is_current",
        "featured",
        "is_visible",
        "display_order",
    )
    list_editable = ("featured", "is_visible", "display_order")
    list_filter = ("kind", "is_current", "featured", "is_visible")
    search_fields = ("role", "organization", "summary", "highlights")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Role", {"fields": ("role", "organization", "kind", "location")}),
        (
            "Dates",
            {"fields": ("date_label", "start_date", "end_date", "is_current")},
        ),
        ("Details", {"fields": ("summary", "highlights", "organization_url")}),
        ("Presentation", {"fields": ("featured", "is_visible", "display_order")}),
        ("History", {"fields": ("created_at", "updated_at")}),
    )


admin.site.site_header = "Bahar Barghbani portfolio administration"
admin.site.site_title = "Portfolio admin"
admin.site.index_title = "Manage academic portfolio content"
