from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image



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
        (KITCHENWARE_AND_APPLIANCES, "kitchenware and appliances"),
        (ARTS_AND_CRAFTS, "arts and crafts"),
        (BABY_AND_KIDS, "baby and kids"),
        (BEAUTY_AND_HEALTH, "beauty and health"),
        (BIKES, "bikes"),
        (BOOKS, "books"),
        (CELL_PHONES, "cell phones"),
        (CLOTHING, "clothing"),
        (COLLECTIBLES, "collectibles"),
        (COMPUTERS, "computers"),
        (ELECTRONICS, "electronics"),
        (GARDEN, "garden"),
        (FURNITURE, "furniture"),
        (FREE, "free"),
        (GENERAL, "general"),
        (HOUSEHOLD, "household"),
        (PETS, "pets"),
        (JEWELERY, "jewelery"),
        (MATERIALS, "materials"),
        (MUSICAL_INSTRUMENTS, "musical instruments"),
        (CAMERA, "cameras"),
        (TOOLS, "tools"),
        (GAMES, "games"),
    ]

    BUY_OR_SELL = [
        (BUY, "I'm a buyer"),
        (SELL, "I'm a seller"),
        (TRADE, 'I want to trade')
    ]

    CONDITION = [
        (NEW, 'The item is brand new.'),
        (LIKE_NEW, 'The item is almost like new.'),
        (USED, 'The item is used. There are minor blemishes or signs of wear.'),
        (FAIR, 'The item is used. There are signs of wear or damage.'),
        (NOT_APPLICABLE, 'N/A')
    ]

    COSMETIC_DAMAGE = [
        (NO_COSMETIC_DAMAGE, 'There are no cosmetic defects'),
        (MINOR, 'There are few cosmetic defects'),
        (MAJOR, 'There are significant cosmetic defects'),
        (NOT_APPLICABLE, 'N/A')
    ]

    title = models.CharField(max_length=60, help_text="Do not include price or location in your title, you can input these details below!")
    image_1 = models.ImageField(default='default_ad.jpg', help_text="This image will be displayed as the main image for your ad.", upload_to='buy_and_sell_ad_images')
    image_2 = models.ImageField(default='default_ad.jpg', help_text="Upload a second image. Try to get provide a different angle.", upload_to='buy_and_sell_ad_images')
    image_3 = models.ImageField(default='default_ad.jpg', help_text="Upload a third image. Try to get provide a different angle.", upload_to='buy_and_sell_ad_images')
    items_or_model_names = models.CharField(max_length=70, help_text="What are you interested in buying or selling?")
    category = models.CharField(max_length=70, choices=CATEGORIES, default=GENERAL, help_text="Choose a category for your ad listing.")
    buying_or_selling = models.CharField(max_length=30, choices=BUY_OR_SELL, default=SELL, help_text="Are you buying or selling?")
    condition = models.CharField(max_length=70, choices=CONDITION, default=NOT_APPLICABLE, help_text="Describe the condition of your item")
    cosmetic_damage = models.CharField(max_length=40, choices=COSMETIC_DAMAGE, default=NOT_APPLICABLE, help_text="Describe the degree of cosmetic damage.")
    asking_price = models.IntegerField(help_text="What is your initial asking price in rubles? (₽)")
    location = models.CharField(max_length=30, help_text="Where are you located?")
    willing_to_travel = models.BooleanField()
    twitter_contact = models.BooleanField(help_text="Can people respond to you via your Twitter? (you can update the link from your profile page)")
    instagram_contact = models.BooleanField(help_text="Can people respond to you via your Instagram? (you can update the link from your profile page)")
    facebook_contact = models.BooleanField(help_text="Can people respond to you via your Facebook? (you can update the link from your profile page)")
    description = models.TextField(max_length=1200, help_text="Write your ad here.")
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

    title = models.CharField(max_length=60, help_text="This is the title that will be displayed on the job board.")
    image = models.ImageField(default='default.jpg', help_text="Upload an image. This image will be displayed above your ad.", upload_to='job_ad_images')
    title_of_position = models.CharField(max_length=70, help_text="What is the title of the position Ex. 'English teacher'?")
    position_type = models.CharField(max_length=50, choices=POSITION_TYPE, default=FULL_TIME, help_text="Please select 'full-time', 'part-time', or 'hourly'.")
    experience = models.CharField(max_length=100, choices=EXPERIENCE, help_text="How much experience is required?")
    education = models.BooleanField(help_text="Is a university degree required?")
    salary = models.IntegerField(help_text="Desired salary or hourly wage (₽).")
    location = models.CharField(max_length=100, help_text="State the job location.")
    involves_travel = models.BooleanField(help_text="Does the job involve travel?")
    name = models.CharField(max_length=100, help_text="State the name of your company, or your name.")
    skype_id = models.CharField(max_length=100, help_text="Provide your Skype ID if you wished to be contacted via skype.")
    email = models.CharField(max_length=100, help_text="Provide an email where applicants can reach you.")
    company_website = models.CharField(max_length=100, default="N/A", help_text="Provide your website url if applicable.")
    company_description = models.TextField(max_length=1000, help_text="Describe your company. Do not describe the job details here!")
    job_description = models.TextField(max_length=3000, help_text="Describe the job description here.")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s, by %s' % (self.title, self.author)


class AdEmail(models.Model):
    """
    Allows users to click the email button on ads, fill out the email form and then have tastyburps email server dispatch the email. This way, users don't need to publically disclose their email to anybody, as the email address is retrievable via the database.
    """
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500, help_text="Write your message here.")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

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
        messages.add_message(self.request, messages.SUCCESS, 'Your email has been successfully posted!')
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