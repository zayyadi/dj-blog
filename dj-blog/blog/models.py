import os

from uuid import uuid4

from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from blog.search import update_index
from core.settings import AUTH_USER_MODEL as User
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings

from django_summernote.fields import SummernoteTextField

# from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

from django.db.models.signals import post_save


# class CustomUser(AbstractUser):
#     user_type_data = ((1, "Admin"), (2, "Editor"), (3, "reader"))
#     user_type = models.CharField(default=3, choices=user_type_data, max_length=10)


def path_and_rename(instance, filename):
    upload_to = "article_pics"
    ext = filename.split(".")[-1]
    # get filename
    if instance.pk:
        filename = "{}.{}".format(instance.pk, ext)
    else:
        # set filename as random string
        filename = "{}.{}".format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("blog:category", args=[self.slug])

    def __str__(self):
        return self.name


class Article(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = SummernoteTextField()
    image = models.ImageField(upload_to=path_and_rename, default="article/default.jpg")
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=options, default="draft")
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    snippet = models.CharField(max_length=255)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ["-publish"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("blog:detail", args=[self.slug])

    def get_tags(self):
        """names() is a django-taggit method, returning a ValuesListQuerySet
        (basically just an iterable) containing the name of each tag as a string
        """
        return self.tags.names()

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)


class Comment(MPTTModel): # Inherit from MPTTModel
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # This is the new field that creates the hierarchy
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        # Sort comments by their creation date
        order_insertion_by = ['created_at']

    def __str__(self):
        # A more descriptive string representation for threaded comments
        if self.parent:
            return f'Reply to {self.parent.user.get_username()} by {self.user.get_username()}'
        return f'Comment by {self.user.get_username()} on {self.post.title}'

LIKE_CHOICES = (
    ("Like", "Like"),
    ("Unlike", "Unlike"),
)


@receiver(post_save, sender=Article)
def update_search_index(sender, instance, **kwargs):
    update_index(instance)


# @receiver(post_migrate)
# def create_search_index(sender, **kwargs):
#     create_index()
