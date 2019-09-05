from django.urls import path
from .views import (
    PostListView,
    PostListViewRussian,
    PostDetailView,
    PostFilter,
    CommentCreateView,
    CommentListView,
    MapView,
    LifeBlogDetailView,
    LifeBlogCommentCreateView,
    LifeBlogFilter,
    about,
    about_ru
)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('blog/filtered/', PostFilter, name='blog-search'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('about/', about, name='blog-about'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='post-comment'),
    path('post/<int:pk>/allcomments/', CommentListView.as_view(), name='comment-list'),
    path('life/<int:pk>/comment/', LifeBlogCommentCreateView.as_view(), name='life-blog-comment'),
    path('map/', MapView.as_view(), name='blog-map'),
    path('life/<int:pk>/', LifeBlogDetailView.as_view(), name='life-blog-detail'),
    path('blog/life/filtered/', LifeBlogFilter, name='life-blog-search'),
    
    #Russian pages
    path('ru/', PostListViewRussian.as_view(), name='blog-home-ru'),
    path('about/ru/', about_ru, name='blog-about-ru'),
]
