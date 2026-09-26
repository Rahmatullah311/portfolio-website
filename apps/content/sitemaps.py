# apps/content/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Article, CodeSnippet, GalleryItem


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return [
            "home",
            "project_list",
            "article_list",
            "snippet_list",
            "gallery_list",
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class ArticleSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CodeSnippetSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return CodeSnippet.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class GallerySitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return GalleryItem.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()
