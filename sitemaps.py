from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import (
  FoodBlog,
  LifeBlog,
)
from users.models import (
  Profile,
  User
)
from classifieds.models import (
  Ad,
  Job
)


class PostSitemap(Sitemap):
  
  def items(self):
    return FoodBlog.objects.all()


class LifeBlogSitemap(Sitemap):
  
  def items(self):
    return LifeBlog.objects.all()


class StaticViewSitemap(Sitemap):

    def items(self):
      static_pages = [
        'blog-home',
        'blog-about',
        'blog-search',
        'life-blog-search',
        'blog-map',
        'register',
        'login',
        'logout',
        'profile',
        'ad-create',
        'ad-list',
        'job-list',
        'faq',
      ]

      return static_pages

    def location(self,item):
      return reverse(item)


class AdSitemap(Sitemap):
  
  def items(self):
    return Ad.objects.all()


class JobSitemap(Sitemap):
  
  def items(self):
    return Job.objects.all()