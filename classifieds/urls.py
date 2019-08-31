from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
  AdCreateView, 
  AdListView,
  AdDetailView,
  AdUpdateView,
  AdDeleteView,
  JobCreateView,
  JobListView,
  JobDetailView,
  JobUpdateView,
  JobDeleteView,
  SendEmailCreateView,
  FaqView
)

urlpatterns = [
  # buy and sell boards
  path('create/', AdCreateView.as_view(), name='ad-create'),
  path('', AdListView, name='ad-list'),
  path('ad/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
  path('ad/<int:pk>/update/', AdUpdateView.as_view(), name='ad-update'),
  path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),

  # jobs
  path('create/jobs-ad/', JobCreateView.as_view(), name='job-wanted-create'),
  path('jobs/', JobListView, name='jobs-list'),
  path('job-ad/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
  path('job-ad/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
  path('job-ad/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),

  path('email/<int:pk>/', SendEmailCreateView.as_view(), name='send-email'),
  path('faq/', FaqView, name='faq'),
]