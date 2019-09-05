from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from PIL import Image


class Profile(models.Model):

    ENGLISH = 'English'
    RUSSIAN = 'Russian'

    LANGUAGE = [
        (ENGLISH, 'English'),
        (RUSSIAN, 'Russian')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics', help_text="*For the best looking profile picture, use a 1:1 size ratio. Images will be rescaled to 150x150 pixels!")
    twitter_link = models.CharField(max_length=150, help_text="Links your twitter URL to your comments. You can optionally enable people to respond to your classified ads, via twitter.", default="https://twitter.com", blank=True)
    instagram_link = models.CharField(max_length=150, help_text="Links your instagram URL to your comments. You can optionally enable people to respond to your classified ads, via instagram", default="https://www.instagram.com", blank=True)
    facebook_link = models.CharField(max_length=150, help_text="Links your facebook URL to your comments. You can optionally enable people to respond to your classified ads, via facebook", default="https://www.facebook.com", blank=True)
    language = models.CharField(max_length=30, choices=LANGUAGE, default=ENGLISH, help_text="(Blogs are written in English first.")
    subscribe_to_food_blogs = models.BooleanField(default=True, help_text='Do you wish to be notified with an email when a new food blog post is published?')
    subscribe_to_Life_in_Moscow_blogs = models.BooleanField(default=True, help_text='Do you wish to be notified with an email when a new "Life in Moscow" blog is published?')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        
        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)
