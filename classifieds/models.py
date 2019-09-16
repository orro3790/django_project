from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class JobBanner(models.Model):

    title = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption = models.TextField(blank=True, max_length=200, help_text='Creates a caption over the image.')
    image = models.ImageField(blank=False, help_text='This image will be displayed as the banner (2560 x 720).', upload_to='job_banners', default='')

    # Russian fields
    title_russian = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption_russian = models.TextField(blank=True, max_length=200, help_text='Creates a Russian caption over the image.')

    def __str__(self):
        return self.title


class BuyAndSellBanner(models.Model):

    title = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption = models.TextField(blank=True, max_length=200, help_text='Creates a caption over the image.')
    image = models.ImageField(blank=False, help_text='This image will be displayed as the banner (2560 x 720).', upload_to='buy_and_sell_banners', default='')

    # Russian fields
    title_russian = models.CharField(blank=True, max_length=100, help_text='This is the title that will be displayed over the caption.')
    caption_russian = models.TextField(blank=True, max_length=200, help_text='Creates a Russian caption over the image.')

    def __str__(self):
        return self.title


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
        (NEW, _('New')),
        (LIKE_NEW, _('Like new')),
        (USED, _('Used')),
        (FAIR, _('Broken or not fully functional')),
        (NOT_APPLICABLE, _('N/A'))
    ]

    COSMETIC_DAMAGE = [
        (NO_COSMETIC_DAMAGE, _('There are no cosmetic defects')),
        (MINOR, _('There are few cosmetic defects')),
        (MAJOR, _('There are significant cosmetic defects')),
        (NOT_APPLICABLE, _('N/A'))
    ]
    
    title = models.CharField(max_length=150, help_text=_("Do not include price or location in your title, you can input these details below!"), verbose_name=_('title'))
    main_image = models.ImageField(default='default_ad.jpg', help_text=_("This image will be displayed as the main image for your ad."), verbose_name=_('Main Image'))
    image_2 = models.ImageField(blank=True, default='', help_text=_("Upload a second image. Try to get provide a different angle."), verbose_name=_('Image 2'))
    image_3 = models.ImageField(blank=True, default='', help_text=_("Upload a third image. Try to get provide a different angle."), verbose_name=_('Image 3'))
    item_or_model_names = models.CharField(max_length=70, help_text=_("What is the exact model name of the item?"), verbose_name=_('Item or Model Name(s)'))
    category = models.CharField(max_length=70, choices=CATEGORIES, default=GENERAL, help_text=_("Choose a category for your ad listing."), verbose_name=_('Category'))
    buying_or_selling = models.CharField(max_length=30, choices=BUY_OR_SELL, default=SELL, help_text=_("Are you buying or selling?"), verbose_name=_('Buying or Selling?'))
    condition = models.CharField(max_length=70, choices=CONDITION, default=NOT_APPLICABLE, help_text=_("Describe the condition of your item"), verbose_name=_('Condition'))
    cosmetic_damage = models.CharField(max_length=40, choices=COSMETIC_DAMAGE, default=NOT_APPLICABLE, help_text=_("Describe the degree of cosmetic damage."), verbose_name=_('cosmetic_damage'))
    asking_price = models.IntegerField(help_text=_("What is your initial asking price in rubles? (₽)"), verbose_name=_('Asking Price'))
    location = models.CharField(max_length=30, help_text=_("Where are you located?"), verbose_name=_('location'))
    willing_to_travel = models.BooleanField(verbose_name=_('Are You Willing to Travel?'))
    twitter_contact = models.BooleanField(help_text=_("Can people respond to you via your Twitter? (you can update the link from your profile page)"), verbose_name=_('Twitter Contact'))
    vk_contact = models.BooleanField(help_text=_("Can people respond to you via your VK? (you can update the link from your profile page)"), verbose_name=_('VK Contact'))
    instagram_contact = models.BooleanField(help_text=_("Can people respond to you via your Instagram? (you can update the link from your profile page)"), verbose_name=_('Instagram Contact'))
    facebook_contact = models.BooleanField(help_text=_("Can people respond to you via your Facebook? (you can update the link from your profile page)"), verbose_name=_('Facebook Contact'))
    description = models.TextField(max_length=1200, help_text=_("Write your ad here."), verbose_name=_('Ad Description'))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return '%s, by %s' % (self.title, self.author)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        main_image = Image.open(self.main_image.path)

        if main_image.height > 1080 or main_image.width > 1080:
            output_size = (1080, 1080)
            main_image.thumbnail(output_size)
            main_image.save(self.main_image.path)

        # Allow image 2 to be deleted
        try:
            image_2 = Image.open(self.image_2.path)
        except Exception:
            image_2 = None
        else:
            if image_2.height > 1080 or image_2.width > 1080:
                output_size = (1080, 1080)
                image_2.thumbnail(output_size)
                image_2.save(self.image_2.path)

        # Allow image 3 to be deleted
        try:
            image_3 = Image.open(self.image_3.path)
        except Exception:
            image_3 = None
        else:
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

    # These attributes can be displayed in the templates'
    PART_TIME = 'Part-time'
    FULL_TIME = 'Full-time'
    VOLUNTEER = 'Volunteer'
    ONE_YEAR = '0-1 year'
    TWO_YEARS = '1-2 years'
    THREE_YEARS = '2-3 years'
    FOUR_YEARS = '3-4 years'
    FIVE_YEARS = '4-5 years'
    FIVE_PLUS = '5+ years'


    EXPERIENCE = [
        (ONE_YEAR, _('0-1 year')),
        (TWO_YEARS, _('1-2 years')),
        (THREE_YEARS, _('2-3 years')),
        (FOUR_YEARS, _('3-4 years')),
        (FIVE_YEARS, _('4-5 years')),
        (FIVE_PLUS, _('5+ years'))
    ]

    POSITION_TYPE = [
        (PART_TIME, _('Part-time')),
        (FULL_TIME, _('Full-time')),
        (VOLUNTEER, _('Volunteer'))
    ]


    title = models.CharField(max_length=60, help_text=_("This is the title that will be displayed on the job board."), verbose_name=_('Title'))
    main_image = models.ImageField(default='default_ad.jpg', help_text=_("Upload an image. This image will be displayed beside your ad."), verbose_name=_('Image or Company Logo'))
    image_2 = models.ImageField(blank=True, default='', help_text=_("Upload a second image (optional)"), verbose_name=_('Image 2'))
    image_3 = models.ImageField(blank=True, default='', help_text=_("Upload a third image (optional)"), verbose_name=_('Image 3'))
    title_of_position = models.CharField(max_length=70, help_text=_("What is the title of the position Ex. 'English teacher'?"), verbose_name=_('Title of Job Position'))
    position_type = models.CharField(max_length=50, choices=POSITION_TYPE, default=FULL_TIME, help_text=_("Please select 'Full-time','Part-time' or 'Volunteer"), verbose_name=_('position_type'))
    experience = models.CharField(max_length=100, choices=EXPERIENCE, help_text=_("How much experience is required?"), verbose_name=_('Experience'))
    degree_required = models.BooleanField(help_text=_("Is a university degree required?"), verbose_name=_('Degree Required'))
    salary = models.IntegerField(blank=False, help_text=_("Proposed salary or hourly wage (₽)."), verbose_name=_('Monthly Salary'), default=50000)
    location = models.CharField(max_length=120, null=True, blank=True, help_text=_("State the job location"), verbose_name=_('Job Location'), default='Moscow')
    involves_travel = models.BooleanField(help_text=_("Does the job involve travel?"), verbose_name=_('Does the Job Involve Travel?'))
    company_name = models.CharField(blank=True, max_length=100, help_text=_("State the name of your company."), verbose_name=_('Company Name'))
    skype_id = models.CharField(blank=True, max_length=100, help_text=_("Provide your Skype ID if you wished to be contacted via skype."), verbose_name=_('Skype ID'))
    company_website = models.URLField(blank=True, max_length=100, default="N/A", help_text=_("Provide your website url if applicable. Example: https://www.whattheblin.com"), verbose_name=_('Company Website'))
    job_description = models.TextField(max_length=3000, help_text=_("Describe the job you are offering."), 
    verbose_name=_('Job Description'))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s, by %s' % (self.title, self.author)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        main_image = Image.open(self.main_image.path)

        if main_image.height > 1080 or main_image.width > 1080:
            output_size = (1080, 1080)
            main_image.thumbnail(output_size)
            main_image.save(self.main_image.path)

        # Allow image 2 to be deleted
        try:
            image_2 = Image.open(self.image_2.path)
        except Exception:
            image_2 = None
        else:
            if image_2.height > 1080 or image_2.width > 1080:
                output_size = (1080, 1080)
                image_2.thumbnail(output_size)
                image_2.save(self.image_2.path)

        # Allow image 3 to be deleted
        try:
            image_3 = Image.open(self.image_3.path)
        except Exception:
            image_3 = None
        else:
            if image_3.height > 1080 or image_3.width > 1080:
                output_size = (1080, 1080)
                image_3.thumbnail(output_size)
                image_3.save(self.image_3.path)

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
        messages.add_message(self.request, messages.SUCCESS, _('Your email has been successfully sent!'))
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