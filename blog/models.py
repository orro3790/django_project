from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

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


# Russian models
class RussianBlogCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        # Display the plural form correctly in the admin panel
        verbose_name_plural = "Russian blog categories"

    def __str__(self):
        return self.name


class RussianTag(models.Model):
    # Russian topic tags for life blogs
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RussianPriceRating(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RussianStoreType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RussianStation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RussianSpecialFeature(models.Model):
    name = models.CharField(max_length=520)

    def __str__(self):
        return self.name


class FoodBlog(models.Model):

    ENGLISH = 'English'
    RUSSIAN = 'Russian'

    LANGUAGE = [
        (ENGLISH, 'English'),
        (RUSSIAN, 'Russian')
    ]

    # Text fields
    title = models.CharField(max_length=100)
    overall_rating = models.ManyToManyField(OverallRating)
    card_content = models.TextField(help_text='This is the preview text shown on the card.', default=None, max_length=300)
    the_good = models.TextField(help_text='Write a short summary describing the good features', max_length=500)
    the_bad = models.TextField(help_text='Write a short summary describing the bad features', max_length=500)
    paragraph_1 = models.TextField(blank=True, help_text='Paragraph 1', default=None, max_length=3000)
    paragraph_2 = models.TextField(blank=True, help_text='Paragraph 2', default=None, max_length=3000)
    paragraph_3 = models.TextField(blank=True, help_text='Paragraph 3', default=None, max_length=3000)
    paragraph_4 = models.TextField(blank=True, help_text='Paragraph 4', default=None, max_length=3000)
    paragraph_5 = models.TextField(blank=True, help_text='Paragraph 5', default=None, max_length=3000)

    # Image fields
    banner = models.ImageField(blank=False, help_text='This is the banner at the top of the page (2560 x 720).', upload_to='food_blog_banners', default='')
    mobile_banner = models.ImageField(blank=False, help_text='This is the mobile version of the banner (600 x 600)', upload_to='food_blog_mobile_banners', default='')
    card_image = models.ImageField(blank=False, default='', upload_to='food_blog_card_images')
    snapshot_1 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_1_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 1.')
    snapshot_2 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_2_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 2.')
    snapshot_3 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_3_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 3.')
    snapshot_4 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_4_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 4.')
    snapshot_5 = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots')
    snapshot_5_B = models.ImageField(blank=True, default='', upload_to='food_blog_snapshots', help_text='This is an optional image, placed beside snapshot 1.')

    # Metric fields
    store_type = models.ManyToManyField(StoreType)
    nearest_station = models.ManyToManyField(Station)
    taste_rating = models.ManyToManyField(TasteRating)
    appearance_rating = models.ManyToManyField(AppearanceRating)
    atmosphere_rating = models.ManyToManyField(AtmosphereRating)
    service_rating = models.ManyToManyField(ServiceRating)
    price_rating = models.ManyToManyField(PriceRating)
    special_feature = models.ManyToManyField(SpecialFeature)

    # Russian fields
    title_russian = models.CharField(blank=True, max_length=100)
    card_content_russian = models.TextField(blank=True, help_text='This is the preview text shown on the card.', default=None, max_length=300)
    the_good_russian = models.TextField(blank=True, help_text='Write a short summary describing the good features', max_length=500)
    the_bad_russian = models.TextField(blank=True, help_text='Write a short summary describing the bad features', max_length=500)
    paragraph_1_russian = models.TextField(blank=True, help_text='Paragraph 1', default=None, max_length=3000)
    paragraph_2_russian = models.TextField(blank=True, help_text='Paragraph 2', default=None, max_length=3000)
    paragraph_3_russian = models.TextField(blank=True, help_text='Paragraph 3', default=None, max_length=3000)
    paragraph_4_russian = models.TextField(blank=True, help_text='Paragraph 4', default=None, max_length=3000)
    paragraph_5_russian = models.TextField(blank=True, help_text='Paragraph 5', default=None, max_length=3000)
    store_type_russian = models.ManyToManyField(RussianStoreType, blank=True)
    nearest_station_russian = models.ManyToManyField(RussianStation, blank=True)
    special_feature_russian = models.ManyToManyField(RussianSpecialFeature, blank=True)
    price_rating_russian = models.ManyToManyField(RussianPriceRating, blank=True)
    publish_translated_blog = models.BooleanField(help_text='When enabled, the Russian post will become visible for Russian users. Keep unchecked until the blog has been fully translated.', default=False)

    # Emails
    send_emails_russian = models.BooleanField(default=False, help_text='When selected, ANY saved changes will trigger the email server to send notifications to all RUSSIAN subscribers that a new post was made. Always create posts with this option unselected first, to ensure no mistakes, then come back and check it.')
    email_message_russian = models.TextField(null=True, blank=True, default=None, max_length=2000, help_text="You can add an optional comment that will be attached in the emails that will be sent to the RUSSIAN subscriber list (Any major corrections or personalized messages, holiday greetings, etc.)")
    send_emails_english = models.BooleanField(default=False, help_text='When selected, ANY saved changes will trigger the email server to send notifications to all subscribers that a new post was made. Always create posts with this option unselected first, to ensure no mistakes, then come back and check it.')
    email_message_english = models.TextField(null=True, blank=True, default=None, max_length=2000, help_text="You can add an optional comment that will be attached in the emails that will be sent to the subscriber list (Any major corrections or personalized messages, holiday greetings, etc.)")

    # Meta fields
    google_map = models.CharField(blank=True, default='Ex: https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2244.6833389633666!2d37.60298461590133!3d55.76400288055638!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46b54bfc8bcfdc57%3A0x9fc4876420a8dffc!2sRestoran+Kafe+Pushkin%22!5e0!3m2!1sen!2sca!4v1559308017720!5m2!1sen!2sca', max_length=600)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog post instance.
        """
        return reverse('post-detail', kwargs={'pk': self.pk})



def save_food_blog(sender, instance, **kwargs):

    # Instance URL
    instance_url_path = instance.get_absolute_url()
    blog_link = 'https://www.whattheblin.com'+(instance_url_path)


    # Query subscriber list:
    subscribers = Profile.objects.all().filter(subscribe_to_food_blogs=True).filter(language='English')
    subscribers_russian = Profile.objects.all().filter(subscribe_to_food_blogs=True).filter(language='Russian')
    
    # English emails
    automated_subject = 'A New Food Blog is Out!: %s' % (instance.title)
    automated_message = 'What The Blin has a new food blog for you! Have you been to '+ instance.title +'? \n \nRead our blog post about it at '+ blog_link +". Leave a comment at the bottom of the blog to tell us what you think, especially if you've been there too (we want to know your favorite menu item from " + instance.title + ", in case we haven't tried it!) \n \nBy the way, if you are tired of getting these notifications, log in to your profile at https://www.whattheblin.com/profile and uncheck the 'Subscribe to food blogs' field. Thanks for supporting us, and enjoy!"

    # Russian emails
    automated_subject_russian = 'Новый блог о еде вышел !: %s' % (instance.title)
    automated_message_russian = 'У нас есть новый блог о еде: '+ instance.title +'! \n \nПрочитайте наш блог об этом здесь: '+ blog_link +". Оставьте комментарий внизу блога, чтобы рассказать нам, что вы думаете.\n \nКстати, если вы не хотите получать эти уведомления, снимите флажок «Подписаться на блоги» в своем профиле. Спасибо за поддержку!"

    # Send emails for English users
    if instance.send_emails_english == True:
        if instance.email_message_english:
            for profile in subscribers:
                send_mail(
                        automated_subject,
                        instance.email_message_english,
                        'notifications@whattheblin.com',
                        [profile.user.email],
                        fail_silently=False
                        )
        else:
            for profile in subscribers:
                send_mail(
                        automated_subject,
                        automated_message,
                        'notifications@whattheblin.com',
                        [profile.user.email],
                        fail_silently=False
                        )
    
    # Send emails for Russian users
    if instance.send_emails_russian == True:
        if instance.email_message_russian:
            for profile in subscribers_russian:
                send_mail(
                        automated_subject_russian,
                        instance.email_message_russian,
                        'notifications@whattheblin.com',
                        [profile.user.email],
                        fail_silently=False
                        )
        else:
            for profile in subscribers_russian:
                send_mail(
                        automated_subject_russian,
                        automated_message_russian,
                        'notifications@whattheblin.com',
                        [profile.user.email],
                        fail_silently=False
                        )


# parameters = (Event function, Model that triggers the desired function)
post_save.connect(save_food_blog, sender=FoodBlog)


class Comment(models.Model):
    
    """
    Model representing a comment against a blog post.
    """
    comment = models.TextField(max_length=500, help_text=_("Post your comment here."), verbose_name=_('comment'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
     # Foreign Key used because PostComment can only have one author/User, but users can have multiple comments
    date_posted = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(FoodBlog, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)+' : '+self.comment[:200]+' — '+str(self.author)


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        # Display the plural form correctly in the admin panel
        verbose_name_plural = "Blog categories"

    def __str__(self):
        return self.name


class LifeBlog(models.Model):

    ENGLISH = 'English'
    RUSSIAN = 'Russian'

    LANGUAGE = [
        (ENGLISH, 'English'),
        (RUSSIAN, 'Russian')
    ]

    # Text fields
    title = models.CharField(max_length=100)
    card_content = models.TextField(default='', help_text="This is the small preview paragraph that will be shown on the card.", max_length=300)
    paragraph_1 = models.TextField(blank=True, help_text='Paragraph 1', default=None, max_length=3000)
    paragraph_2 = models.TextField(blank=True, help_text='Paragraph 2', default=None, max_length=3000)
    paragraph_3 = models.TextField(blank=True, help_text='Paragraph 3', default=None, max_length=3000)
    paragraph_4 = models.TextField(blank=True, help_text='Paragraph 4', default=None, max_length=3000)
    paragraph_5 = models.TextField(blank=True, help_text='Paragraph 5', default=None, max_length=3000)

    # Image fields
    card_image = models.ImageField(blank=True, default='', upload_to='life_blog_card_images')
    banner = models.ImageField(blank=False, help_text='This is the banner at the top of the page (2560 x 720).', upload_to='life_blog_banners', default='')
    mobile_banner = models.ImageField(blank=False, help_text='This is the mobile version of the banner (600 x 600)', upload_to='life_blog_banners_mobile', default='')
    snapshot_1 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_1_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 1.')
    snapshot_2 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_2_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 2.')
    snapshot_3 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_3_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 3.')
    snapshot_4 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_4_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 4.')
    snapshot_5 = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots')
    snapshot_5_B = models.ImageField(blank=True, default='', upload_to='life_blog_snapshots', help_text='This is an optional image, placed beside snapshot 5.')

    # Russian fields
    title_russian = models.CharField(max_length=100, blank=True)
    card_content_russian = models.TextField(default='Write your article here!', max_length=300, blank=True)
    paragraph_1_russian = models.TextField(help_text='Paragraph 1', default=None, max_length=3000, blank=True)
    paragraph_2_russian = models.TextField(help_text='Paragraph 2', default=None, max_length=3000, blank=True)
    paragraph_3_russian = models.TextField(help_text='Paragraph 3', default=None, max_length=3000, blank=True)
    paragraph_4_russian = models.TextField(help_text='Paragraph 4', default=None, max_length=3000, blank=True)
    paragraph_5_russian = models.TextField(help_text='Paragraph 5', default=None, max_length=3000, blank=True)
    blog_category_russian = models.ManyToManyField(RussianBlogCategory, blank=True)
    tags_russian = models.ManyToManyField(RussianTag, blank=True)
    publish_translated_blog = models.BooleanField(help_text='When enabled, the Russian post will become visible for Russian users. Keep unchecked until the blog has been fully translated.', default=False)
    
    # Emails
    send_emails_english = models.BooleanField(default=False, help_text='When selected, ANY saved changes will trigger the email server to send notifications to all ENGLISH subscribers that a new post was made. Always create posts with this option unselected first, to ensure no mistakes, then come back and check it.')
    email_message_english = models.TextField(blank=True, null=True, default=None, max_length=2000, help_text="You can add an optional comment that will be attached in the emails that will be sent to the ENGLISH subscriber list (Any major corrections or personalized messages, holiday greetings, etc.)")
    send_emails_russian = models.BooleanField(default=False, help_text='When selected, ANY saved changes will trigger the email server to send notifications to all RUSSIAN subscribers that a new post was made. Always create posts with this option unselected first, to ensure no mistakes, then come back and check it.')
    email_message_russian = models.TextField(blank=True, null=True, default=None, max_length=2000, help_text="You can add an optional comment that will be attached in the emails that will be sent to the RUSSIAN subscriber list (Any major corrections or personalized messages, holiday greetings, etc.)")

    # Meta
    blog_category = models.ManyToManyField(BlogCategory, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    google_map = models.CharField(blank=True, default='Ex: https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2244.6833389633666!2d37.60298461590133!3d55.76400288055638!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46b54bfc8bcfdc57%3A0x9fc4876420a8dffc!2sRestoran+Kafe+Pushkin%22!5e0!3m2!1sen!2sca!4v1559308017720!5m2!1sen!2sca', max_length=600)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular blog post instance.
        """
        return reverse('life-blog-detail', kwargs={'pk': self.pk})


def save_life_blog(sender, instance, **kwargs):

    # Instance URL
    instance_url_path = instance.get_absolute_url()
    blog_link = 'https://www.whattheblin.com'+(instance_url_path)


    # Query subscriber list:
    subscribers = Profile.objects.all().filter(subscribe_to_Life_in_Moscow_blogs=True).filter(language="English")
    subscribers_russian = Profile.objects.all().filter(subscribe_to_Life_in_Moscow_blogs=True).filter(language="Russian")

    # English emails
    automated_subject = 'A New "Life in Moscow" Blog is Out: %s' % (instance.title)
    automated_message = 'What The Blin has a new "Life in Moscow" blog for you, called '+ instance.title +'! \n \nRead it here at '+ blog_link +". Leave a comment at the bottom of the blog to tell us what you think. Your feedback helps us tremendously. We hope you enjoy it! \n \nBy the way, if you are tired of getting these notifications, log in to your profile at https://www.whattheblin.com/profile and uncheck the 'Subscribe to Life in Moscow blogs' field. Thanks for supporting us!"

    # Russian emails
    automated_subject_russian = 'Новый блог «Жизнь в Москве» вышел: %s' % (instance.title)
    automated_message_russian = 'Для чего у Blin появился новый блог «Жизнь в Москве»:'+ instance.title +'! \n \nПрочитайте наш блог об этом здесь: '+ blog_link +". Оставьте комментарий внизу блога, чтобы рассказать нам, что вы думаете.\n \nКстати, если вы не хотите получать эти уведомления, снимите флажок «Подписаться на блоги» в своем профиле. Спасибо за поддержку!"

    
    # Send emails for English users
    if instance.send_emails_english == True:
        if instance.email_message_english:
            for profile in subscribers:
                send_mail(
                        automated_subject,
                        instance.email_message_english,
                        'notifications@whattheblin.com',
                        [profile.user.email],
                        fail_silently=False
                        )
        else:
            for profile in subscribers:
                send_mail(
                        automated_subject,
                        automated_message,
                        'notifications@whattheblin.com',
                        [profile.user.email],
                        fail_silently=False
                        )
    
    # Send emails for Russian users
    if instance.send_emails_russian == True:
        if instance.email_message_russian:
            for profile in subscribers_russian:
                send_mail(
                        automated_subject_russian,
                        instance.email_message_russian,
                        'notifications@whattheblin.com',
                        [profile.user.email],
                        fail_silently=False
                        )
        else:
            for profile in subscribers_russian:
                send_mail(
                        automated_subject_russian,
                        automated_message_russian,
                        'notifications@whattheblin.com',
                        [profile.user.email],
                        fail_silently=False
                        )


# parameters = (Event function, Model that triggers the desired function)
post_save.connect(save_life_blog, sender=LifeBlog)


class LifeBlogComment(models.Model):
    
    """
    Model representing a comment against a life blog post.
    """
    comment = models.TextField(max_length=500, help_text=_("Post your comment here."), verbose_name=_('comment'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
     # Foreign Key used because PostComment can only have one author/User, but users can have multiple comments
    date_posted = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(LifeBlog, on_delete=models.CASCADE)

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


    SLIDE_NUMBER = [
    ('First', 'First Slide'),
    ('Second', 'Second Slide'),
    ('Third', 'Third Slide'),
    ]


    slide_number = models.CharField(max_length=100, choices=SLIDE_NUMBER, default='First Slide')
    title = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption = models.TextField(blank=True, max_length=200, help_text='Creates a caption over the image.')
    image = models.ImageField(blank=False, help_text='This image will be displayed as the banner (2560 x 720).', upload_to='food_blog_search_banners', default='')
    link = models.CharField(blank=True, max_length=200, help_text='Optionally, attach a link.')

    # Russian fields
    title_russian = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption_russian = models.TextField(blank=True, max_length=200, help_text='Creates a Russian caption over the image.')
    link_russian = models.CharField(blank=True, max_length=200, help_text='Optionally, attach a link for Russian users.')

    def __str__(self):
        return self.slide_number


class LifeBlogSearchBanner(models.Model):


    SLIDE_NUMBER = [
    ('First', 'First Slide'),
    ('Second', 'Second Slide'),
    ('Third', 'Third Slide'),
    ]

    slide_number = models.CharField(max_length=100, choices=SLIDE_NUMBER, default='First Slide')
    title = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption = models.TextField(blank=True, max_length=200, help_text='Creates a caption over the image.')
    image = models.ImageField(blank=False, help_text='This image will be displayed as the banner (2560 x 720).', upload_to='life_blog_search_banners', default='')
    link = models.CharField(blank=True, max_length=200, help_text='Optionally, attach a link.')

    # Russian fields
    title_russian = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption_russian = models.TextField(blank=True, max_length=200, help_text='Creates a Russian caption over the image.')
    link_russian = models.CharField(blank=True, max_length=200, help_text='Optionally, attach a link for Russian users.')

    def __str__(self):
        return self.slide_number


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

