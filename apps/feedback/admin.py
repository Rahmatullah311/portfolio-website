from django.contrib import admin
from django.utils.html import format_html
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("content_object", "content_type", "rating_stars", "created_at")
    list_filter = ("rating", "content_type", "created_at")
    search_fields = ("comment",)
    readonly_fields = (
        "content_type",
        "object_id",
        "rating",
        "comment",
        "user",
        "created_at",
    )

    fieldsets = (
        (
            "Feedback Details",
            {"fields": ("content_type", "object_id", "rating", "comment")},
        ),
        ("Metadata", {"fields": ("user", "created_at"), "classes": ("collapse",)}),
    )

    def rating_stars(self, obj):
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        return format_html('<span style="color: #f0ad4e;">{}</span>', stars)

    rating_stars.short_description = "Rating"

    def has_add_permission(self, request):
        return False
