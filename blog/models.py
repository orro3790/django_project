from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile


class StoreType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SpecialFeature(models.Model):
    name = models.CharField(max_length=520)

    def __str__(self):
        return self.name


class OverallRating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return str(self.rating)


class TasteRating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return str(self.rating)


class AppearanceRating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return str(self.rating)


class AtmosphereRating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return str(self.rating)


class ServiceRating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return str(self.rating)


class PriceRating(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    # Topic tags for life blogs
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):

    ENGLISH = 'English'
    RUSSIAN = 'Russian'

    LANGUAGE = [
        (ENGLISH, 'English'),
        (RUSSIAN, 'Russian')
    ]

    banner = models.ImageField(blank=False, help_text='This is the banner at the top of the page (2560 x 720).', upload_to='food_blog_banners', default='')
    mobile_banner = models.ImageField(blank=False, help_text='This is the mobile version of the banner (600 x 600)', upload_to='food_blog_mobile_banners', default='')
    card_image = models.ImageField(blank=False, default='', upload_to='food_blog_card_images')
    title = models.CharField(max_length=100)
    overall_rating = models.ManyToManyField(OverallRating)
    card_content = models.TextField(help_text='This is the preview text shown on the card.', default=None, max_length=300)
    the_good = models.TextField(help_text='Write a short summary describing the good features', max_length=500)
    the_bad = models.TextField(help_text='Write a short summary describing the bad features', max_length=500)
    paragraph_1 = models.TextField(help_text='Paragraph 1', default=None, max_length=3000)
    snapshot_1 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_1_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 1.')
    paragraph_2 = models.TextField(help_text='Paragraph 2', default=None, max_length=3000)
    snapshot_2 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_2_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 2.')
    paragraph_3 = models.TextField(help_text='Paragraph 3', default=None, max_length=3000)
    snapshot_3 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_3_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 3.')
    paragraph_4 = models.TextField(help_text='Paragraph 4', default=None, max_length=3000)
    snapshot_4 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_4_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 4.')
    paragraph_5 = models.TextField(help_text='Paragraph 5', default=None, max_length=3000)
    snapshot_5 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_5_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 1.')
    store_type = models.ManyToManyField(StoreType)
    nearest_station = models.ManyToManyField(Station)
    taste_rating = models.ManyToManyField(TasteRating)
    appearance_rating = models.ManyToManyField(AppearanceRating)
    atmosphere_rating = models.ManyToManyField(AtmosphereRating)
    service_rating = models.ManyToManyField(ServiceRating)
    price_rating = models.ManyToManyField(PriceRating)
    special_feature = models.ManyToManyField(SpecialFeature)
    language = models.CharField(max_length=30, choices=LANGUAGE, default=ENGLISH, help_text="Is this post in English, or Russian?")
    translated_blog_link = models.CharField(blank=True, default='', max_length=500, help_text="If the blog exists in only one language, leave this field blank.")
    google_map = models.CharField(default='Ex: https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2244.6833389633666!2d37.60298461590133!3d55.76400288055638!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46b54bfc8bcfdc57%3A0x9fc4876420a8dffc!2sRestoran+Kafe+Pushkin%22!5e0!3m2!1sen!2sca!4v1559308017720!5m2!1sen!2sca', blank=False, max_length=600)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog post instance.
        """
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    
    """
    Model representing a comment against a blog post.
    """
    comment = models.TextField(max_length=500, help_text="Post your comment in here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
     # Foreign Key used because PostComment can only have one author/User, but users can have multiple comments
    date_posted = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.post)+' : '+self.comment[:200]+' — '+str(self.author)


class BlogType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LifeBlog(models.Model):

    ENGLISH = 'English'
    RUSSIAN = 'Russian'

    LANGUAGE = [
        (ENGLISH, 'English'),
        (RUSSIAN, 'Russian')
    ]

    card_image = models.ImageField(blank=True, default='', upload_to='life_blog_card_images')
    title = models.CharField(max_length=100)
    card_content = models.TextField(default='Write your article here!', max_length=300)
    banner = models.ImageField(blank=False, help_text='This is the banner at the top of the page (2560 x 720).', upload_to='life_blog_banners', default='')
    mobile_banner = models.ImageField(blank=False, help_text='This is the mobile version of the banner (600 x 600)', upload_to='life_blog_banners_mobile', default='')
    paragraph_1 = models.TextField(default='Paragraph 1', max_length=3000)
    snapshot_1 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_1_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 1.')
    paragraph_2 = models.TextField(default='Paragraph 1', max_length=3000)
    snapshot_2 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_2_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 2.')
    paragraph_3 = models.TextField(default='Paragraph 1', max_length=3000)
    snapshot_3 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_3_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 3.')
    paragraph_4 = models.TextField(default='Paragraph 1', max_length=3000)
    snapshot_4 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_4_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 4.')
    paragraph_5 = models.TextField(default='Paragraph 1', max_length=3000)
    snapshot_5 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_5_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 5.')
    blog_type = models.ManyToManyField(BlogType)
    language = models.CharField(max_length=30, choices=LANGUAGE, default=ENGLISH, help_text="Is this post in English, or Russian?")
    translated_blog_link = models.CharField(blank=True, default='', max_length=500, help_text="If the blog exists in only one language, leave this field blank.")
    google_map = models.CharField(blank=True, default='', max_length=600)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog post instance.
        """
        return reverse('life-blog-detail', kwargs={'pk': self.pk})




class LifeBlogComment(models.Model):
    
    """
    Model representing a comment against a blog post.
    """
    comment = models.TextField(max_length=500, help_text="Post your comment in here.")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
     # Foreign Key used because PostComment can only have one author/User, but users can have multiple comments
    date_posted = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(LifeBlog, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.post)+' : '+self.comment[:200]+' — '+str(self.author)


class AboutUsPicture(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='about_us')

    def __str__(self):
        return self.name


class CarouselImage(models.Model):

    SLIDE_NUMBER = [
    ('First', 'First Slide'),
    ('Second', 'Second Slide'),
    ('Third', 'Third Slide'),
    ]

    slide_number = title = models.CharField(max_length=100, choices=SLIDE_NUMBER, default='First Slide')
    title = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption = models.TextField(blank=True, max_length=200, help_text='The caption goes here.')
    image = models.ImageField(blank=False, help_text='This image will be displayed in the carousel (2560 x 720).', upload_to='carousel_images', default='')
    mobile_image = models.ImageField(blank=False, help_text='This image will be displayed in the carousel when viewed on cellphones (600 x 600).', upload_to='carousel_images', default='')
    link = models.CharField(blank=True, max_length=200, help_text='Ex: https://www.brave.com/features/')

    # Russian settings
    title_russian = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption_russian = models.TextField(blank=True, max_length=200, help_text='The caption goes here.')
    link_russian = models.CharField(blank=True, max_length=200, help_text='Ex: https://www.brave.com/features/')

    def __str__(self):
        return self.title


class FoodSearchBanner(models.Model):

    BANNER_STATUS = [
    ('Display', 'Display'),
    ('Hide', 'Hide')
    ]

    visibility = models.CharField(max_length=100, choices=BANNER_STATUS, default='Display', help_text="If inactive, the banner will not be displayed but can remain stored as a backup. Must select active to display.")
    caption = models.TextField(blank=True, max_length=200, help_text='Creates a caption over the image.')
    image = models.ImageField(blank=False, help_text='This image will be displayed as the banner (2560 x 720).', upload_to='food_blog_search_banners', default='')
    link = models.CharField(blank=True, max_length=200, help_text='Optionally, attach a link.')

    def __str__(self):
        return self.caption


class LifeBlogSearchBanner(models.Model):

    BANNER_STATUS = [
    ('Display', 'Display'),
    ('Hide', 'Hide')
    ]

    visibility = models.CharField(max_length=100, choices=BANNER_STATUS, default='Display', help_text="If inactive, the banner will not be displayed but can remain stored as a backup. Must select active to display.")
    caption = models.TextField(blank=True, max_length=200, help_text='Creates a caption over the image.')
    image = models.ImageField(blank=False, help_text='This image will be displayed as the banner (2560 x 720).', upload_to='life_blog_search_banners', default='')
    link = models.CharField(blank=True, max_length=200, help_text='Optionally, attach a link.')

    def __str__(self):
        return self.caption


class AboutUsBanner(models.Model):

    BANNER_STATUS = [
    ('Display', 'Display'),
    ('Hide', 'Hide')
    ]

    visibility = models.CharField(max_length=100, choices=BANNER_STATUS, default='Display', help_text="If inactive, the banner will not be displayed but can remain stored as a backup. Must select active to display.")
    caption = models.TextField(blank=True, max_length=200, help_text='Creates a caption over the image.')
    image = models.ImageField(blank=False, help_text='This image will be displayed as the banner (2560 x 720).', upload_to='life_blog_search_banners', default='')
    link = models.CharField(blank=True, max_length=200, help_text='Optionally, attach a link.')

    def __str__(self):
        return self.caption


class FoodMap(models.Model):

    link = models.CharField(blank=True, max_length=200, help_text='Optionally, attach a link.')

    def __str__(self):
        return self.link