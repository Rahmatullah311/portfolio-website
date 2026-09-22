from django.contrib import admin
from django import forms
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from .models import Project, Article, CodeSnippet, GalleryItem


# Custom Admin Forms with CKEditor
class ProjectAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name="default"))

    class Meta:
        model = Project
        fields = "__all__"


class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name="default"))

    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "content": CKEditorWidget(attrs={"class": "ckeditor"}),
        }

    class Media:
        css = {"all": ("admin/css/ckeditor-dark.css",)}


class CodeSnippetAdminForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = "__all__"
        widgets = {
            "code": forms.Textarea(
                attrs={
                    "class": "code-editor",
                    "style": 'font-family: "Fira Code", "Courier New", monospace; background: #1e1e1e; color: #d4d4d4; padding: 20px; min-height: 500px; border-radius: 8px; font-size: 14px; line-height: 1.6;',
                    "spellcheck": "false",
                }
            )
        }


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ("title", "featured_status", "created_at")
    list_filter = ("featured", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20

    fieldsets = (
        (
            "Project Information",
            {
                "fields": ("title", "slug", "description", "featured"),
                "classes": ("wide",),
            },
        ),
        (
            "Project Content",
            {"fields": ("content",), "classes": ("wide", "extrapretty")},
        ),
        (
            "Technical Stack",
            {
                "fields": ("tech_stack",),
                "description": "Enter technologies separated by commas (e.g., React, Node.js, MongoDB)",
            },
        ),
        ("Project Links", {"fields": ("demo_url", "github_url")}),
        ("Project Image", {"fields": ("image",)}),
    )

    def featured_status(self, obj):
        if obj.featured:
            return format_html('<span style="color: #10b981;">✓ Featured</span>')
        return format_html('<span style="color: #6b7280;">—</span>')

    featured_status.short_description = "Featured"

    def save_model(self, request, obj, form, change):
        # Convert comma-separated tech stack to list
        if isinstance(obj.tech_stack, str):
            obj.tech_stack = [
                tech.strip() for tech in obj.tech_stack.split(",") if tech.strip()
            ]
        super().save_model(request, obj, form, change)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ("title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20

    fieldsets = (
        (
            "Article Information",
            {"fields": ("title", "slug", "tags"), "classes": ("wide",)},
        ),
        (
            "Article Content",
            {"fields": ("content",), "classes": ("wide", "extrapretty")},
        ),
    )

    def save_model(self, request, obj, form, change):
        # Convert comma-separated tags to list
        if isinstance(obj.tags, str):
            obj.tags = [tag.strip() for tag in obj.tags.split(",") if tag.strip()]
        super().save_model(request, obj, form, change)


@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    form = CodeSnippetAdminForm
    list_display = ("title", "language", "created_at")
    list_filter = ("language", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 20

    fieldsets = (
        (
            "Snippet Information",
            {
                "fields": ("title", "slug", "language", "description", "tags"),
                "classes": ("wide",),
            },
        ),
        ("Code Editor", {"fields": ("code",), "classes": ("wide", "extrapretty")}),
    )

    def save_model(self, request, obj, form, change):
        # Convert comma-separated tags to list
        if isinstance(obj.tags, str):
            obj.tags = [tag.strip() for tag in obj.tags.split(",") if tag.strip()]
        super().save_model(request, obj, form, change)


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "created_at")
    list_filter = ("type", "created_at")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at",)
    list_per_page = 20

    fieldsets = (
        (
            "Media Information",
            {"fields": ("title", "slug", "type", "description"), "classes": ("wide",)},
        ),
        ("Media Source", {"fields": ("url", "image"), "classes": ("wide",)}),
    )
