from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



class Ad(models.Model):

    # These attributes can be displayed in the templates
    BUY = "I'm a buyer"
    SELL = "I'm a seller"
    TRADE = 'I want to trade'

    NEW = 'New'
    LIKE_NEW = 'Like new'
    USED = 'Used'
    FAIR = 'Fair'

    NO_COSMETIC_DAMAGE = 'None'
    MINOR = 'Minor'
    MAJOR = 'Major'
    NOT_APPLICABLE = 'N/A'

    KITCHENWARE_AND_APPLIANCES = "kitchenware and appliances"
    ARTS_AND_CRAFTS = "arts and crafts"
    BABY_AND_KIDS = "baby and kids"
    BEAUTY_AND_HEALTH = "beauty and health"
    BIKES = "bikes"
    BOOKS = "books"
    CELL_PHONES = "cell phones"
    CLOTHING = "clothing"
    COLLECTIBLES = "collectibles"
    COMPUTERS = "computers"
    ELECTRONICS = "electronics"
    GARDEN = "garden"
    FREE = "free"
    GENERAL = 'general'
    HOUSEHOLD = "household"
    PETS = "pets"
    FURNITURE = "furniture"
    JEWELERY = "jewelery"
    MATERIALS = "materials"
    MUSICAL_INSTRUMENTS = "musical instruments"
    CAMERA = "cameras"
    TOOLS = "tools"
    GAMES = "games"

    CATEGORIES = [
        (KITCHENWARE_AND_APPLIANCES, _("kitchenware and appliances")),
        (ARTS_AND_CRAFTS, _("arts and crafts")),
        (BABY_AND_KIDS, _("baby and kids")),
        (BEAUTY_AND_HEALTH, _("beauty and health")),
        (BIKES, _("bikes")),
        (BOOKS, _("books")),
        (CELL_PHONES, _("cell phones")),
        (CLOTHING, _("clothing")),
        (COLLECTIBLES, _("collectibles")),
        (COMPUTERS, _("computers")),
        (ELECTRONICS, _("electronics")),
        (GARDEN, _("garden")),
        (FURNITURE, _("furniture")),
        (FREE, _("free")),
        (GENERAL, _("general")),
        (HOUSEHOLD, _("household")),
        (PETS, _("pets")),
        (JEWELERY, _("jewelery")),
        (MATERIALS, _("materials")),
        (MUSICAL_INSTRUMENTS, _("musical instruments")),
        (CAMERA, _("cameras")),
        (TOOLS, _("tools")),
        (GAMES, _("games")),
    ]

    BUY_OR_SELL = [
        (BUY, _("I'm a buyer")),
        (SELL, _("I'm a seller")),
        (TRADE, _('I want to trade'))
    ]

    CONDITION = [
        (NEW, _('The item is brand new.')),
        (LIKE_NEW, _('The item is almost like new.')),
        (USED, _('The item is used. There are minor blemishes or signs of wear.')),
        (FAIR, _('The item is used. There are signs of wear or damage.')),
        (NOT_APPLICABLE, _('N/A'))
    ]

    COSMETIC_DAMAGE = [
        (NO_COSMETIC_DAMAGE, _('There are no cosmetic defects')),
        (MINOR, _('There are few cosmetic defects')),
        (MAJOR, _('There are significant cosmetic defects')),
        (NOT_APPLICABLE, _('N/A'))
    ]

    title = models.CharField(max_length=60, help_text=_("Do not include price or location in your title, you can input these details below!"), verbose_name=_('title'))
    image_1 = models.ImageField(default='default_ad.jpg', help_text=_("This image will be displayed as the main image for your ad."), verbose_name=_('image'))
    image_2 = models.ImageField(default='default_ad.jpg', help_text=_("Upload a second image. Try to get provide a different angle."), verbose_name=_('image_2'))
    image_3 = models.ImageField(default='default_ad.jpg', help_text=_("Upload a third image. Try to get provide a different angle."), verbose_name=_('image_3'))
    items_or_model_names = models.CharField(max_length=70, help_text=_("What are you interested in buying or selling?"), verbose_name=_('items_or_model_names'))
    category = models.CharField(max_length=70, choices=CATEGORIES, default=GENERAL, help_text=_("Choose a category for your ad listing."), verbose_name=_('category'))
    buying_or_selling = models.CharField(max_length=30, choices=BUY_OR_SELL, default=SELL, help_text=_("Are you buying or selling?"), verbose_name=_('buying or selling'))
    condition = models.CharField(max_length=70, choices=CONDITION, default=NOT_APPLICABLE, help_text=_("Describe the condition of your item"), verbose_name=_('condition'))
    cosmetic_damage = models.CharField(max_length=40, choices=COSMETIC_DAMAGE, default=NOT_APPLICABLE, help_text=_("Describe the degree of cosmetic damage."), verbose_name=_('cosmetic_damage'))
    asking_price = models.IntegerField(help_text=_("What is your initial asking price in rubles? (₽)"), verbose_name=_('asking_price'))
    location = models.CharField(max_length=30, help_text=_("Where are you located?"), verbose_name=_('location'))
    willing_to_travel = models.BooleanField(verbose_name=_('willing_to_travel'))
    twitter_contact = models.BooleanField(help_text=_("Can people respond to you via your Twitter? (you can update the link from your profile page)"), verbose_name=_('twitter_contact'))
    instagram_contact = models.BooleanField(help_text=_("Can people respond to you via your Instagram? (you can update the link from your profile page)"), verbose_name=_('instagram_contact'))
    facebook_contact = models.BooleanField(help_text=_("Can people respond to you via your Facebook? (you can update the link from your profile page)"), verbose_name=_('facebook_contact'))
    description = models.TextField(max_length=1200, help_text=_("Write your ad here."), verbose_name=_('description'))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s, by %s' % (self.title, self.author)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image_1 = Image.open(self.image_1.path)
        image_2 = Image.open(self.image_2.path)
        image_3 = Image.open(self.image_3.path)
        
        if image_1.height > 1080 or image_1.width > 1080:
            output_size = (1080, 1080)
            image_1.thumbnail(output_size)
            image_1.save(self.image_1.path)

        if image_2.height > 1080 or image_2.width > 1080:
            output_size = (1080, 1080)
            image_2.thumbnail(output_size)
            image_2.save(self.image_2.path)
            
        if image_3.height > 1080 or image_3.width > 1080:
            output_size = (1080, 1080)
            image_3.thumbnail(output_size)
            image_3.save(self.image_3.path)

    def get_absolute_url(self):
        """
        Returns the url to access a particular ad instance.
        """
        return reverse('ad-detail', kwargs={'pk': self.pk})

        
class Job(models.Model):

    # These attributes can be displayed in the templates
    SEEKING_JOB = 'I am seeking a job.'
    OFFERING_JOB = 'I am offering a job.'
    PART_TIME = 'part-time'
    FULL_TIME = 'full-time'
    HOURLY = 'hourly'
    ONE_YEAR = '0-1 year'
    TWO_YEARS = '1-2 years'
    THREE_YEARS = '2-3 years'
    FOUR_YEARS = '3-4 years'
    FIVE_YEARS = '4-5 years'
    FIVE_PLUS = '5+ years'

    EXPERIENCE = [
        (ONE_YEAR, '0-1 year'),
        (TWO_YEARS, '1-2 years'),
        (THREE_YEARS, '2-3 years'),
        (FOUR_YEARS, '3-4 years'),
        (FIVE_YEARS, '4-5 years'),
        (FIVE_PLUS, '5+ years')
    ]

    JOBS = [
        (SEEKING_JOB, 'I am seeking a job.'),
        (OFFERING_JOB, 'I am offering a job.')
    ]

    POSITION_TYPE = [
        (PART_TIME, 'part-time'),
        (FULL_TIME, 'full-time'),
        (HOURLY, 'hourly')
    ]

    title = models.CharField(max_length=60, help_text=_("This is the title that will be displayed on the job board."), verbose_name=_('title'))
    image = models.ImageField(default='default.jpg', help_text=_("Upload an image. This image will be displayed above your ad."), verbose_name=_('image'))
    title_of_position = models.CharField(max_length=70, help_text=_("What is the title of the position Ex. 'English teacher'?"), verbose_name=_('title_of_position'))
    position_type = models.CharField(max_length=50, choices=POSITION_TYPE, default=FULL_TIME, help_text=_("Please select 'full-time', 'part-time', or 'hourly'."), verbose_name=_('position_type'))
    experience = models.CharField(max_length=100, choices=EXPERIENCE, help_text=_("How much experience is required?"), verbose_name=_('experience'))
    education = models.BooleanField(help_text=_("Is a university degree required?"), verbose_name=_('education'))
    salary = models.IntegerField(help_text=_("Desired salary or hourly wage (₽)."), verbose_name=_('salary'))
    location = models.CharField(max_length=100, help_text=_("State the job location."), verbose_name=_('location'))
    involves_travel = models.BooleanField(help_text=_("Does the job involve travel?"), verbose_name=_('involves_travel'))
    name = models.CharField(max_length=100, help_text=_("State the name of your company, or your name."), verbose_name=_('name'))
    skype_id = models.CharField(blank=True, max_length=100, help_text=_("Provide your Skype ID if you wished to be contacted via skype."), verbose_name=_('skype_id'))
    email = models.CharField(max_length=100, help_text=_("Provide an email where applicants can reach you."), verbose_name=_('email'))
    company_website = models.CharField(blank=True, max_length=100, default="N/A", help_text=_("Provide your website url if applicable."), verbose_name=_('company_website'))
    company_description = models.TextField(max_length=1000, help_text=_("Describe your company. Do not describe the job details here!"), verbose_name=_('company_description'))
    job_description = models.TextField(max_length=3000, help_text=_("Describe the job description here."), verbose_name=_('job_description'))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s, by %s' % (self.title, self.author)

    def get_absolute_url(self):
        """
        Returns the url to access a particular job instance.
        """
        return reverse('job-detail', kwargs={'pk': self.pk})


class AdEmail(models.Model):
    """
    Allows users to click the email button on ads, fill out the email form and then have tastyburps email server dispatch the email. This way, users don't need to publically disclose their email to anybody, as the email address is retrievable via the database.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    description = models.TextField(max_length=500, help_text=_("Write your message here."), verbose_name=_('description'))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name=_('ad'))

    def get_context_data(self, **kwargs):
        """
        Add associated ad to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the ad from id and add it to the context
        context['ad'] = get_object_or_404(Ad, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form, *args, **kwargs):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.ad=get_object_or_404(Ad, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super().form_valid(form)
   
    def get_success_url(self): 
        """
        After posting comment, provide success message and return to associated blog post.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your email has been successfully posted!'))
        return reverse('ad-list', kwargs={'pk': self.kwargs['pk'],})

    def __str__(self):
        return '%s, by %s' % (self.title, self.author)


class Buyer(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name