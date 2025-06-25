import os

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from blog.sitemaps import PostSitemap

sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path(os.getenv("ADMIN_INTERNAL_URL"), admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path(
        "",
        include("blog.urls", namespace="blog"),
    ),
    path(
        "users/",
        include("users.urls", namespace="users"),
    ),
    path(
        "__reload__/",
        include("django_browser_reload.urls"),
    ),
    path(
        "oauth/",
        include("social_django.urls", namespace="social"),
    ),
    path(
        "summernote/",
        include("django_summernote.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
