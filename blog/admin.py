from django.contrib import admin
from .models import (
  Post,
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
  BlogType,
  Tag,
  CarouselImage,
  FoodSearchBanner,
  LifeBlogSearchBanner,
  AboutUsBanner,
  FoodMap
)

# Clean up the Post layout page in the admin console

class PostAdmin(admin.ModelAdmin):
  fieldsets = [
    ("Card", {"fields": ["card_image","title", "card_content"]}),
    ("Blog Article", {"fields": ["banner", "mobile_banner", "the_good", "the_bad", "paragraph_1", "snapshot_1", "snapshot_1_B", "paragraph_2", "snapshot_2", "snapshot_2_B", "paragraph_3", "snapshot_3", "snapshot_3_B", "paragraph_4", "snapshot_4", "snapshot_4_B", "paragraph_5", "snapshot_5", "snapshot_5_B",]}),
    ("Ratings and Location", {"fields": ["taste_rating", "appearance_rating", "atmosphere_rating", "price_rating",
    "service_rating", "overall_rating","special_feature", "store_type", "nearest_station", "google_map", "language", "translated_blog_link"]}),
    ("Meta", {"fields": ["date_posted"]})
  ]

  def save_model(self, request, obj, form, change):
    obj.author = request.user
    obj.save()



class LifeBlogAdmin(admin.ModelAdmin):
  fieldsets = [
    ("Card", {"fields": ["card_image","title", "card_content"]}),
    ("Blog Article", {"fields": ["banner", "mobile_banner", "blog_type", "paragraph_1", "snapshot_1", "snapshot_1_B", "paragraph_2", "snapshot_2", "snapshot_2_B", "paragraph_3", "snapshot_3", "snapshot_3_B", "paragraph_4", "snapshot_4", "snapshot_4_B", "paragraph_5", "snapshot_5", "snapshot_5_B", "language", "translated_blog_link"]}),
    ("Location", {"fields": ["google_map"]}),
    ("Meta", {"fields": ["date_posted","tags"]})
  ]

  def save_model(self, request, obj, form, change):
    obj.author = request.user
    obj.save()



# Let's register this model to the admin site, so we can view these posts from the admin panel online
admin.site.register(Post, PostAdmin)
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
admin.site.register(BlogType)
admin.site.register(Tag)
admin.site.register(LifeBlogComment)
admin.site.register(CarouselImage)
admin.site.register(FoodSearchBanner)
admin.site.register(LifeBlogSearchBanner)
admin.site.register(AboutUsBanner)
admin.site.register(FoodMap)

