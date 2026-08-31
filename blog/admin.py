from django.contrib import admin
from django.utils import timezone

from .models import Post, Comment


admin.site.site_header = "Bahar Barghbani Blog Administration"
admin.site.site_title = "Blog admin"
admin.site.index_title = "Content management"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("post_title", "status", "published_at", "date_posted")
    list_filter = ("status", "published_at", "date_posted")
    search_fields = ("post_title", "post_preview", "content")
    ordering = ("-published_at", "-date_posted", "-id")
    readonly_fields = ("date_posted",)
    actions = ("publish_now", "move_to_draft")
    fieldsets = (
        (
            "Content",
            {
                "fields": ("post_title", "post_preview", "content", "image"),
            },
        ),
        (
            "Publication",
            {
                "fields": ("slug", "status", "published_at", "date_posted"),
            },
        ),
    )

    @admin.action(description="Publish selected posts now")
    def publish_now(self, request, queryset):
        updated = queryset.update(
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        self.message_user(request, f"Published {updated} post(s).")

    @admin.action(description="Move selected posts back to draft")
    def move_to_draft(self, request, queryset):
        updated = queryset.update(
            status=Post.Status.DRAFT,
            published_at=None,
        )
        self.message_user(request, f"Moved {updated} post(s) to draft.")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "date_added")
    search_fields = ("name", "body", "post__post_title")
    list_filter = ("date_added",)
    ordering = ("-date_added",)
