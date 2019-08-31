from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostFilter,
    CommentCreateView,
    CommentListView,
    MapView,
    LifeBlogListView,
    LifeBlogDetailView,
    LifeBlogCommentCreateView,
    LifeBlogFilter
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('blog/filtered/', PostFilter, name='blog-search'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='post-comment'),
    path('post/<int:pk>/allcomments/', CommentListView.as_view(), name='comment-list'),
    path('life/<int:pk>/comment/', LifeBlogCommentCreateView.as_view(), name='life-blog-comment'),
    path('map/', MapView.as_view(), name='blog-map'),
    path('life/', LifeBlogListView.as_view(), name='blog-life'),
    path('life/<int:pk>/', LifeBlogDetailView.as_view(), name='life-blog-detail'),
    path('blog/life/filtered/', LifeBlogFilter, name='life-blog-search'),
]