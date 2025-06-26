from django.urls import path

from blog import views

from .feeds import AtomSiteNewsFeed, LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("addarticle/", views.addArticle, name="addarticle"),
    path("article/<slug:post>/", views.detail, name="detail"),
    path("update/<slug:slug>", views.ArticleUpdateView.as_view(), name="update"),
    path("tag/<slug:slug>/", views.articles, name="tagged"),
    path("delete/<slug:slug>", views.deleteArticle, name="delete"),
    path("", views.articles, name="articles"),
    path("like/<slug:slug>", views.LikeView, name="article_like"),
    path("add_catergory/", views.addCategory, name="add_category"),
    path("category/<slug:category_slug>", views.category, name="category"),
    path("search/", views.search_view, name="search_view"),
    # Comment URLs
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path('approval/queue/', views.draft_list, name='draft_list'),
    path('approval/view/<slug:slug>/', views.draft_detail, name='draft_detail'),
    path('approval/approve/<slug:slug>/', views.approve_article, name='approve_article'),
]
