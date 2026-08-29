from django.contrib import admin

from .models import Post, Comment


admin.site.site_header = "Bahar Barghbani Blog Administration"
admin.site.site_title = "Blog admin"
admin.site.index_title = "Content management"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("post_title", "date_posted")
    search_fields = ("post_title", "post_preview", "content")
    ordering = ("-date_posted", "-id")
    fieldsets = (
        (
            "Post",
            {
                "fields": ("post_title", "post_preview", "content", "image"),
            },
        ),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "date_added")
    search_fields = ("name", "body", "post__post_title")
    list_filter = ("date_added",)
    ordering = ("-date_added",)
