# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.content.sitemaps import (
    StaticViewSitemap,
    ProjectSitemap,
    ArticleSitemap,
    CodeSnippetSitemap,
    GallerySitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "articles": ArticleSitemap,
    "snippets": CodeSnippetSitemap,
    "gallery": GallerySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("apps.content.urls")),
    path("feedback/", include("apps.feedback.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
