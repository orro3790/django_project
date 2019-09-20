from django.urls import path
from .views import (
    FoodBlogListView,
    PostDetailView,
    FoodBlogFilter,
    CommentCreateView,
    CommentListView,
    MapView,
    LifeBlogDetailView,
    LifeBlogCommentCreateView,
    LifeBlogFilter,
    about,
    ThingsWeLoveView
    # Russian views
)

urlpatterns = [
    path('', FoodBlogListView, name='blog-home'),
    path('blog/filtered/', FoodBlogFilter, name='blog-search'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('about/', about, name='blog-about'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='post-comment'),
    path('post/<int:pk>/allcomments/', CommentListView.as_view(), name='comment-list'),
    path('life/<int:pk>/comment/', LifeBlogCommentCreateView.as_view(), name='life-blog-comment'),
    path('map/', MapView.as_view(), name='blog-map'),
    path('thingswelove/', ThingsWeLoveView.as_view(), name='things-we-love'),
    path('life/<int:pk>/', LifeBlogDetailView.as_view(), name='life-blog-detail'),
    path('blog/life/filtered/', LifeBlogFilter, name='life-blog-search'),
]
