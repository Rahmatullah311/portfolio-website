# apps/content/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # Project URLs
    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path(
        "projects/<slug:slug>/",
        views.ProjectDetailView.as_view(),
        name="project_detail",
    ),
    # Article URLs
    path("articles/", views.ArticleListView.as_view(), name="article_list"),
    path(
        "articles/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    # Snippet URLs
    path("snippets/", views.SnippetListView.as_view(), name="snippet_list"),
    path(
        "snippets/<slug:slug>/",
        views.SnippetDetailView.as_view(),
        name="snippet_detail",
    ),
    # Gallery URLs
    path("gallery/", views.GalleryListView.as_view(), name="gallery_list"),
    path(
        "gallery/<slug:slug>/", views.GalleryDetailView.as_view(), name="gallery_detail"
    ),
]
