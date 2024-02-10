import os

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(os.getenv("ADMIN_INTERNAL_URL"), admin.site.urls),
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
