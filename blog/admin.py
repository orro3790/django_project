from django.contrib import admin
from .models import (
  FoodBlog,
  StoreType,
  Station,
  SpecialFeature,
  OverallRating,
  TasteRating,
  AppearanceRating,
  AtmosphereRating,
  ServiceRating,
  PriceRating,
  Comment,
  AboutUsPicture,
  LifeBlog,
  LifeBlogComment,
  BlogCategory,
  Tag,
  CarouselImage,
  FoodSearchBanner,
  LifeBlogSearchBanner,
  AboutUsBanner,
  FoodMap,
  ThingsWeLove,
  # Russian Models
  RussianStoreType,
  RussianStation,
  RussianSpecialFeature,
  RussianBlogCategory,
  RussianTag,
  RussianPriceRating
)
from django.db import models

# Clean up the FoodBlog layout page in the admin console

class PostAdmin(admin.ModelAdmin):
  fieldsets = [
    ("Card", {"fields": ["card_image","title", "card_content"]}),
    ("Blog Article", {"fields": ["banner", "mobile_banner", "the_good", "the_bad", "paragraph_1", "snapshot_1", "snapshot_1_B", "paragraph_2", "snapshot_2", "snapshot_2_B", "paragraph_3", "snapshot_3", "snapshot_3_B", "paragraph_4", "snapshot_4", "snapshot_4_B", "paragraph_5", "snapshot_5", "snapshot_5_B",]}),
    ("Metrics", {"fields": ["taste_rating", "appearance_rating", "atmosphere_rating", "price_rating",
    "service_rating", "overall_rating","special_feature", "store_type", "nearest_station", ]}),
    ("Location Pin", {"fields": ["google_map"]}),
    ("Social Media Share Buttons", {"fields": ["twitter_card_image"]}),

    # Russian fields
    ("Russian Card", {"fields": ["title_russian", "card_content_russian"]}),
    ("Russian Blog Article", {"fields": ["the_good_russian", "the_bad_russian", "paragraph_1_russian", "paragraph_2_russian", "paragraph_3_russian", "paragraph_4_russian", "paragraph_5_russian"]}),
    ("Russian Metrics", {"fields": ["special_feature_russian", "store_type_russian", "nearest_station_russian", 'price_rating_russian']}),
    ("Publish Russian Version", {"fields": ["publish_translated_blog"]}),
    ("Send Emails", {"fields": ["send_emails_english", "email_message_english", 'send_emails_russian', 'email_message_russian']}),
  ]

  def save_model(self, request, obj, form, change):
    obj.author = request.user
    obj.save()


class LifeBlogAdmin(admin.ModelAdmin):
  fieldsets = [
    ("Card", {"fields": ["card_image","title", "card_content"]}),
    ("Blog Article", {"fields": ["banner", "mobile_banner", "paragraph_1", "snapshot_1", "snapshot_1_B", "paragraph_2", "snapshot_2", "snapshot_2_B", "paragraph_3", "snapshot_3", "snapshot_3_B", "paragraph_4", "snapshot_4", "snapshot_4_B", "paragraph_5", "snapshot_5", "snapshot_5_B"]}),
    ("Location", {"fields": ["google_map"]}),
    ("Meta Data", {"fields": ["blog_category", "tags"]}),
    ("Subscriber Notifications", {"fields": ["send_emails_english", "email_message_english"]}),

    # Russian fields
    ("Russian Card", {"fields": ["title_russian", "card_content_russian"]}),
    ("Russian Blog Article", {"fields": ["paragraph_1_russian", "paragraph_2_russian", "paragraph_3_russian", "paragraph_4_russian", "paragraph_5_russian"]}),
    ("Russian Meta", {"fields": ["blog_category_russian", "tags_russian"]}),
    ("Publish and Notify Subscribers", {"fields": ["publish_translated_blog"]}),
  ]


  def save_model(self, request, obj, form, change):
    obj.author = request.user
    obj.save()


# Register this model to the admin site, so we can view these posts from the admin panel online
admin.site.register(FoodBlog, PostAdmin)
admin.site.register(StoreType)
admin.site.register(Station)
admin.site.register(SpecialFeature)
admin.site.register(OverallRating)
admin.site.register(TasteRating)
admin.site.register(AppearanceRating)
admin.site.register(AtmosphereRating)
admin.site.register(ServiceRating)
admin.site.register(PriceRating)
admin.site.register(Comment)
admin.site.register(AboutUsPicture)
admin.site.register(LifeBlog, LifeBlogAdmin)
admin.site.register(BlogCategory)
admin.site.register(Tag)
admin.site.register(LifeBlogComment)
admin.site.register(CarouselImage)
admin.site.register(FoodSearchBanner)
admin.site.register(LifeBlogSearchBanner)
admin.site.register(AboutUsBanner)
admin.site.register(FoodMap)
admin.site.register(ThingsWeLove)
admin.site.register(RussianStation)
admin.site.register(RussianStoreType)
admin.site.register(RussianSpecialFeature)
admin.site.register(RussianBlogCategory)
admin.site.register(RussianTag)
admin.site.register(RussianPriceRating)
