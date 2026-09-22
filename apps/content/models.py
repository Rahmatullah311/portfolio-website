from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation


class Project(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the project title")
    slug = models.SlugField(
        unique=True, blank=True, help_text="Auto-generated from title"
    )
    description = models.TextField(help_text="Short summary shown in cards")
    content = models.TextField(help_text="Full details (use the rich text editor)")
    tech_stack = models.JSONField(
        default=list,
        blank=True,
        help_text="Enter technologies separated by commas (e.g., React, Node.js, MongoDB)",
    )
    demo_url = models.URLField(blank=True, null=True, help_text="Live demo URL")
    github_url = models.URLField(
        blank=True, null=True, help_text="GitHub repository URL"
    )
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
        help_text="Project screenshot or image",
    )
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    feedbacks = GenericRelation("feedback.Feedback")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("project_detail", kwargs={"slug": self.slug})


class Article(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the article title")
    slug = models.SlugField(
        unique=True, blank=True, help_text="Auto-generated from title"
    )
    content = models.TextField(
        help_text="Write your article using the rich text editor"
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Enter tags separated by commas (e.g., webdev, javascript, tutorial)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    feedbacks = GenericRelation("feedback.Feedback")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("article_detail", kwargs={"slug": self.slug})


class CodeSnippet(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the snippet title")
    slug = models.SlugField(
        unique=True, blank=True, help_text="Auto-generated from title"
    )
    language = models.CharField(
        max_length=50, help_text="e.g., python, javascript, css"
    )
    code = models.TextField(help_text="Paste your code here")
    description = models.TextField(
        blank=True, help_text="Brief description of what this code does"
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Enter tags separated by commas (e.g., algorithm, performance)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    feedbacks = GenericRelation("feedback.Feedback")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Code Snippet"
        verbose_name_plural = "Code Snippets"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("snippet_detail", kwargs={"slug": self.slug})


class GalleryItem(models.Model):
    TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]
    title = models.CharField(max_length=200, help_text="Enter the media title")
    slug = models.SlugField(
        unique=True, blank=True, help_text="Auto-generated from title"
    )
    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, help_text="Select media type"
    )
    url = models.URLField(
        blank=True, help_text="External URL (YouTube for videos, direct image URL)"
    )
    image = models.ImageField(
        upload_to="gallery/", blank=True, null=True, help_text="Or upload an image"
    )
    description = models.TextField(
        blank=True, help_text="Short description of the media"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    feedbacks = GenericRelation("feedback.Feedback")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("gallery_detail", kwargs={"slug": self.slug})

    @property
    def youtube_embed_url(self):
        """Extract YouTube video ID and return embed URL"""
        if self.type == "video" and "youtube.com/watch?v=" in self.url:
            video_id = self.url.split("v=")[1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return None
