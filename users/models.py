from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from PIL import Image
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):

    ENGLISH = 'English'
    RUSSIAN = 'Russian'

    LANGUAGE = [
        (ENGLISH, 'English'),
        (RUSSIAN, 'Russian')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics', help_text=_("For the best looking profile picture, use a 1:1 size ratio. Images will be rescaled to 150x150 pixels!"), verbose_name=_('image'))
    twitter_link = models.CharField(max_length=150, help_text=_("Links your twitter URL to your comments. You can optionally enable people to respond to your classified ads, via twitter."), default="https://twitter.com", blank=True, verbose_name=_('twitter_link'))
    instagram_link = models.CharField(max_length=150, help_text=_("Links your instagram URL to your comments. You can optionally enable people to respond to your classified ads, via instagram"), default="https://www.instagram.com", blank=True, verbose_name=_('instagram_link'))
    facebook_link = models.CharField(max_length=150, help_text=_("Links your facebook URL to your comments. You can optionally enable people to respond to your classified ads, via facebook"), default="https://www.facebook.com", blank=True, verbose_name=_('facebook_link'))
    language = models.CharField(max_length=30, choices=LANGUAGE, default=ENGLISH, help_text=_("(Blogs are written in English first.)"), verbose_name=_('language'))
    subscribe_to_food_blogs = models.BooleanField(default=True, help_text=_('Do you wish to be notified with an email when a new food blog post is published?'), verbose_name=_('subscribe_to_food_blogs'))
    subscribe_to_Life_in_Moscow_blogs = models.BooleanField(default=True, help_text=_('Do you wish to be notified with an email when a new Life in Moscow blog is published?'), verbose_name=_('subscribe_to_Life_in_Moscow_blogs'))

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        
        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)
