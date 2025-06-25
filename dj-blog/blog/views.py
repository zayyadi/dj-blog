from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from users.models import NewUser
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)  # noqa: F401
from django.template.defaultfilters import slugify
from taggit.models import Tag
from django.http import HttpResponseForbidden
from django_ratelimit.decorators import ratelimit # Added for rate limiting

from blog.search import search
from .models import Article, Category, Comment # Added Comment model

from .forms import ArticleForm, CommentForm, CategoryForm


@login_required
def addCategory(request):
    form = CategoryForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        form.save_m2m()

        messages.success(request, "Category created successfully")
        return redirect("blog:articles")
    context = {
        "form": form,
    }
    return render(request, "blog/addCategory.html", context)


def articles(request, slug=None):
    articles = Article.objects.all().filter(status="published")
    paginator = Paginator(articles, 5)
    page = request.GET.get("page")
    tag = None
    if slug:
        get_object_or_404(Tag, slug=slug)
    # Article.tags.most_common()[:2]
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        "articles": articles,
        "tag": tag,
        "page": page,
    }

    return render(request, "blog/articles.html", context)


@login_required
def LikeView(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.likes.add(request.user)
    return redirect("blog:detail", article.slug)


def about(request):
    return render(request, "blog/about.html")


@login_required
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {"articles": articles}
    return render(request, "blog/dashboard.html", context)


@login_required
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    common_tags = Article.tags.most_common()[:4]
    if form.is_valid():
        article = form.save(commit=False)
        article.slug = slugify(article.title)
        article.author = request.user
        article.save()
        form.save_m2m()

        messages.success(request, "Article created successfully")
        return redirect("blog:dashboard")
    context = {
        "common_tags": common_tags,
        "form": form,
    }
    return render(request, "blog/addarticle.html", context)


@ratelimit(key='ip', rate='10/m', method='POST', block=True) # Rate limit comment posting
def detail(request, post):
    # article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, slug=post, status="published")
    comments = article.comments.all()
    # page = request.GET.get("page", 1)

    # paginator = Paginator(allcomments, 10)
    # try:
    #     comments = paginator.page(page)
    # except PageNotAnInteger:
    #     comments = paginator.page(1)
    # except EmptyPage:
    #     comments = paginator.page(paginator.num_pages)
    article_tags = Article.tags.values_list("id", flat=True)
    similar_posts = Article.objects.filter(tags__in=article_tags).exclude(id=article.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:3]

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = article
            comment.save()
            messages.success(request, "Your comment has been added.")
            return redirect("blog:detail", post=post)
    else:
        form = CommentForm()

    # if request.method == "POST":
    #     comment_form = CommentForm(request.POST)
    #     if comment_form.is_valid():
    #         user_comment = comment_form.save(commit=False)
    #         user_comment.post = article
    #         user_comment.save()
    #         return HttpResponseRedirect(request.path_info)
    # else:
    #     comment_form = CommentForm()

    context = {
        "comments": comments, # Renamed from "comment" to "comments" for clarity
        "comment_form": form,
        "article": article,
        "similar_posts": similar_posts,
    }

    return render(request, "blog/detail.html", context)


# @login_required
# def updateArticle(request, slug):
#     article = get_object_or_404(Article, slug=slug)
#     form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
#     if form.is_valid():
#         article = form.save(commit=False)

#         article.author = request.user
#         article.save()

#         messages.success(request, "Article has been Updated")
#         return redirect("blog:dashboard")
#     return render(request, "blog/update.html", {"form": form})
from django.views.generic import UpdateView  # noqa: E402

class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/update.html'
    context_object_name = 'post' # Add this line


@login_required
def deleteArticle(request, slug):
    article = get_object_or_404(Article, slug=slug)

    article.delete()

    messages.success(request, "Article Deleted Successfully")

    return redirect("blog:dashboard")


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Article.tags.most_common()[:4]
    article = Article.objects.filter(tags=tag)
    context = {
        "tag": tag,
        "common_tags": common_tags,
        "article": article,
    }
    return render(request, "article.html", context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    article = Article.objects.filter(category=category)

    context = {"category": category, "article": article}

    return render(request, "blog/category.html", context)


def category_list(request):
    category_list = Category.objects.exclude(name="default")
    context = {
        "category_list": category_list,
    }
    return context


def search_view(request):
    query = request.GET.get("q")
    if query:
        results = search(query)
    else:
        results = []

    return render(request, "blog/search.html", {"results": results, "query": query})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        # Optionally, allow staff/superusers to edit any comment
        # if not request.user.is_staff:
        #     return HttpResponseForbidden("You are not allowed to edit this comment.")
        return HttpResponseForbidden("You are not allowed to edit this comment.")


    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect("blog:detail", post=comment.post.slug)
    else:
        form = CommentForm(instance=comment)

    return render(
        request, "blog/edit_comment.html", {"form": form, "comment": comment}
    )


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Allow comment owner or staff/superusers to delete
    if comment.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    if request.method == "POST":
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect("blog:detail", post=post_slug)

    return render(request, "blog/delete_comment_confirm.html", {"comment": comment})
