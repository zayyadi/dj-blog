
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(status="published") # Corrected status value

    def lastmod(self, obj):
        return obj.publish # Using publish field, consider adding an 'updated_at' field to Article model

    def location(self, item):
        return reverse(item)