# apps/content/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Project, Article, CodeSnippet, GalleryItem
from apps.feedback.forms import FeedbackForm
from django.contrib.contenttypes.models import ContentType


class HomeView(TemplateView):
    template_name = "content/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_projects"] = Project.objects.filter(featured=True)[:6]
        context["latest_articles"] = Article.objects.all()[:3]
        context["recent_snippets"] = CodeSnippet.objects.all()[:5]
        context["gallery_preview"] = GalleryItem.objects.all()[:8]
        return context


class ProjectListView(ListView):
    model = Project
    template_name = "content/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        queryset = Project.objects.all()
        # Filter by tech stack if provided
        tech = self.request.GET.get("tech")
        if tech:
            queryset = queryset.filter(tech_stack__contains=[tech])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all unique tech stacks for filter buttons
        all_tech = []
        for project in Project.objects.all():
            all_tech.extend(project.tech_stack or [])
        context["all_tech"] = sorted(set(all_tech))
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "content/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_form"] = FeedbackForm()
        context["feedbacks"] = self.object.feedbacks.all()
        context["content_type"] = ContentType.objects.get_for_model(Project)
        return context


class ArticleListView(ListView):
    model = Article
    template_name = "content/article_list.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.all()
        tag = self.request.GET.get("tag")
        if tag:
            queryset = queryset.filter(tags__contains=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_tags = []
        for article in Article.objects.all():
            all_tags.extend(article.tags or [])
        context["all_tags"] = sorted(set(all_tags))
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "content/article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_form"] = FeedbackForm()
        context["feedbacks"] = self.object.feedbacks.all()
        context["content_type"] = ContentType.objects.get_for_model(Article)
        return context


class SnippetListView(ListView):
    model = CodeSnippet
    template_name = "content/snippet_list.html"
    context_object_name = "snippets"
    paginate_by = 20

    def get_queryset(self):
        queryset = CodeSnippet.objects.all()
        language = self.request.GET.get("language")
        if language:
            queryset = queryset.filter(language=language)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_languages"] = CodeSnippet.objects.values_list(
            "language", flat=True
        ).distinct()
        return context


class SnippetDetailView(DetailView):
    model = CodeSnippet
    template_name = "content/snippet_detail.html"
    context_object_name = "snippet"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_form"] = FeedbackForm()
        context["feedbacks"] = self.object.feedbacks.all()
        context["content_type"] = ContentType.objects.get_for_model(CodeSnippet)
        return context


class GalleryListView(ListView):
    model = GalleryItem
    template_name = "content/gallery_list.html"
    context_object_name = "gallery_items"
    paginate_by = 20

    def get_queryset(self):
        queryset = GalleryItem.objects.all()
        item_type = self.request.GET.get("type")
        if item_type:
            queryset = queryset.filter(type=item_type)
        return queryset


class GalleryDetailView(DetailView):
    model = GalleryItem
    template_name = "content/gallery_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_form"] = FeedbackForm()
        context["feedbacks"] = self.object.feedbacks.all()
        context["content_type"] = ContentType.objects.get_for_model(GalleryItem)
        return context
