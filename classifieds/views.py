from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, gettext_noop
from django.contrib.postgres import search
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchQuery
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView
from . models import (
    Ad,
    Job,
    AdEmail,
    Buyer,
    Seller,
    BuyAndSellBanner,
    JobBanner
)
from django import forms
from . forms import (
    AdForm,
    JobForm,
    SendEmailForm,
)


class AdCreateView(LoginRequiredMixin, CreateView):

    model = Ad
    form_class = AdForm

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def get_success_url(self): 
        messages.add_message(self.request, messages.SUCCESS, _('Your ad has been successfully posted!'))
        return reverse('ad-list')


def valid_query(param):
    # makes sure that there is actually a search value and that it is not an empty string
    return param != '' and param is not None


def AdListView(request):

    qs = Ad.objects.all()
    carousel_images = BuyAndSellBanner.objects.all()
    language = get_language()

    # Default ENGLISH placeholder/values for each field in the HTML template:
    default_keyword = ''
    default_category = _('Category...')
    default_role = _('I want to buy / sell...')
    default_price = ''

    # Get the user queries
    keyword_query = request.GET.get('keyword_filter')
    price_query = request.GET.get('price_filter')
    role_query = request.GET.get('role_filter')
    category_query = request.GET.get('category_filter')
    
    if category_query is not None and category_query != default_category:
        category_query = request.GET.get('category_filter').split(' -')[0]
        

    # Outcome #1: Default page load
    if category_query is None and keyword_query is None and price_query is None and role_query is None:
        qs = qs.order_by('-date_posted')

    # Outcome #2: A user presses submit without any values
    if category_query == default_category and role_query == default_role and keyword_query == default_keyword and price_query == default_price:
        qs = qs.order_by('-date_posted')

    # Outcome #3: Individual field searches and combination searches:
    # Create valid search functions for each field, all of which store results as 'qs', allowing chain filtering:
    
    # Contains:
    if keyword_query is not None and keyword_query != default_keyword:
        # Search by value
        search_contains = qs.annotate(search=SearchVector('title', 'description', 'item_or_model_names')).filter(search=keyword_query)
        # Search only by: Contains
        qs = search_contains.order_by('-date_posted')

    # Category:
    if category_query is not None and category_query != default_category:
        
        # Search by value
        if language == 'en':
            search_category = qs.annotate(search=SearchVector('category')).filter(search=category_query)

        # If language is Russian, convert the terms to English so they can pull English equivalents
        elif language == 'ru':

            if category_query == _('arts and crafts'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='arts and crafts')

            elif category_query == _('baby and kids'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='baby and kids')

            elif category_query == _('beauty and health'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='beauty and health')

            elif category_query == _('bikes'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='bikes')

            elif category_query == _('books'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='books') 

            elif category_query == _('cell phones'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='cell phones')
            
            elif category_query == _('clothing'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='clothing')
            
            elif category_query == _('collectibles'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='collectibles')
            
            elif category_query == _('computers'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='computers')
            
            elif category_query == _('electronics'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='electronics')
            
            elif category_query == _('garden'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='garden')
            
            elif category_query == _('furniture'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='furniture')
            
            elif category_query == _('free'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='free')
            
            elif category_query == _('general'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='general')
            
            elif category_query == _('household'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='household') 
            
            elif category_query == _('pets'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='pets')
            
            elif category_query == _('jewelery'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='jewelery')

            elif category_query == _('kitchenware and appliances'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='kitchenware and appliances')
            
            elif category_query == _('materials'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='materials')
            
            elif category_query == _('musical instruments'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='musical instruments')
            
            elif category_query == _('cameras'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='cameras')
            
            elif category_query == _('tools'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='tools')
            
            elif category_query == _('games'):
                search_category = qs.annotate(search=SearchVector('category')).filter(search='games')

            else:
                # handle the error that occurs from language toggling immediately after doing a search 
                return redirect('ad-list')

        # Search only by: Category
        qs = search_category.order_by('-date_posted')
        
    # Role:
    if role_query is not None and role_query != default_role:
        
        if language == 'en':

            if role_query == 'I want to buy':
                # Search by value
                search_role = qs.annotate(search=SearchVector('buying_or_selling')).filter(search="I'm a seller")
                # Search only by: I want to sell
                qs = search_role.order_by('-date_posted')

            elif role_query == 'I want to sell':
                # Search by value
                search_role = qs.annotate(search=SearchVector('buying_or_selling')).filter(search="I'm a buyer")
                # Search only by: I want to sell
                qs = search_role.order_by('-date_posted')

            elif role_query == 'I want to trade':
                # Search by value
                search_role = qs.annotate(search=SearchVector('buying_or_selling')).filter(search="I want to trade")
                # Search only by: I want to trade
                qs = search_role.order_by('-date_posted')
        
            else:
                # handle the error that occurs from language toggling immediately after doing a search 
                return redirect('ad-list')

        elif language == 'ru':
            
            if role_query == _('I want to buy'):
                # Search by value
                search_role = qs.annotate(search=SearchVector('buying_or_selling')).filter(search="I'm a seller")
                # Search only by: I want to sell
                qs = search_role.order_by('-date_posted')

            elif role_query == _('I want to sell'):
                # Search by value
                search_role = qs.annotate(search=SearchVector('buying_or_selling')).filter(search="I'm a buyer")
                # Search only by: I want to sell
                qs = search_role.order_by('-date_posted')

            elif role_query == _('I want to trade'):
                # Search by value
                search_role = qs.annotate(search=SearchVector('buying_or_selling')).filter(search="I want to trade")
                # Search only by: I want to trade
                qs = search_role.order_by('-date_posted')

            else:
                # handle the error that occurs from language toggling immediately after doing a search 
                return redirect('ad-list')

    # Price:
    if price_query is not None and price_query != default_price:
        # Search by value
        search_price = qs.filter(asking_price__lte=price_query)
        # Search only by: Price
        qs = search_price.order_by('-date_posted')

    # paginate
    paginator = Paginator(qs, 20) # controls the # of ads per page
    page = request.GET.get('page')
    qs = paginator.get_page(page)

    context = {
        'ads': qs,
        'carousel_images': carousel_images,
        'keyword_query': keyword_query,
        'category_query': category_query,
        'role_query': role_query,
        'price_query': price_query,
    }

    return render(request, 'classifieds/ad_list.html', context)


class AdDetailView(DetailView):
    model = Ad


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    template_name = 'classifieds/ad_update_form.html'
    context_object_name = 'ad'
    fields = [
        'title',
        'main_image',
        'image_2',
        'image_3',
        'item_or_model_names',
        'category',
        'buying_or_selling',
        'condition',
        'cosmetic_damage',
        'asking_price',
        'location',
        'willing_to_travel',
        'twitter_contact',
        'instagram_contact',
        'facebook_contact',
        'description',
        ]

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ad = self.get_object()
        if self.request.user == ad.author:
            return True
        return False

    def get_success_url(self): 
        """
        After updating ad, provide success message and return to the detail view of associated ad.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your ad has been successfully updated!'))
        return reverse('ad-list')


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'classifieds/ad_confirm_delete.html'
    success_url = 'classifieds/ad_update_form.html'
    context_object_name = 'ad'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self): 
        """
        After deleting ad, provide success message and return to the list of ads.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your ad has been successfully deleted!'))
        return reverse('ad-list')


class JobCreateView(LoginRequiredMixin, CreateView):

    model = Job
    form_class = JobForm

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self): 
        """
        After posting comment, provide success message and return to associated blog post.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your ad has been successfully posted!'))
        return reverse('job-list')


def JobListView(request):

    # Base queries
    qs = Job.objects.all()
    carousel_images = JobBanner.objects.all()
    location_list = Job.objects.all().values_list('location', flat=True).distinct()
    language = get_language()

    # Default placeholder/values for each field as written in the HTML template:
    default_keyword = ''
    default_salary = ''
    default_location = _('Location...')
    default_position = _('Position Type...')

    # Get the user queries
    keyword_query = request.GET.get('keyword_filter')
    salary_query = request.GET.get('salary_filter')
    location_query = request.GET.get('location_filter')
    position_query = request.GET.get('position_filter')

    # Outcome #1: Default page load (tested and handles both en and ru)
    if keyword_query is None and salary_query is None and location_query is None and position_query is None:
        qs = qs.order_by('-date_posted')
        
    # Outcome #2: A user presses submit without any values:efault_salary and location_query == default_location and position_query == default_position:
        qs = qs.order_by('-date_posted')
        
    # Outcome #3: Individual field searches and combination searches:
    # Create valid search functions for each field, all of which store results back into 'qs', allowing chain filtering:

    # Contains:
    if keyword_query is not None and keyword_query != default_keyword:
        qs = qs.annotate(search=SearchVector('title', 'title_of_position', 'job_description')).filter(search=keyword_query).order_by('-date_posted')
        
    # Location:
    if location_query is not None and location_query != default_location:
        qs = qs.annotate(search=SearchVector('location')).filter(search=location_query).order_by('-date_posted')

    # Price:
    if salary_query is not None and salary_query != default_salary:
        # Search by value
        search_salary = qs.filter(salary__gte=salary_query)
        # Search only by: Price
        qs = search_salary.order_by('-date_posted')

    # Position Type
    if position_query is not None and position_query != default_position:

        if language == 'en':
            if position_query == _('All-paid'):
                qs = qs.exclude(position_type__icontains='Volunteer')
            elif position_query == _('Part-time'):
                qs = qs.annotate(search=SearchVector('position_type')).filter(search='Part-time').order_by('-date_posted')
            elif position_query == _('Volunteer'):
                qs = qs.annotate(search=SearchVector('position_type')).filter(search='Volunteer').order_by('-date_posted')
            elif position_query == _('Full-time'):
                qs = qs.annotate(search=SearchVector('position_type')).filter(search='Full-time').order_by('-date_posted')
            else:
                # handle the error that occurs from language toggling immediately after doing a search 
                return redirect('job-list')

        if language == 'ru':
            if position_query == _('All-paid'):
                qs = qs.exclude(position_type__icontains='Volunteer')
            elif position_query == _('Part-time'):
                qs = qs.annotate(search=SearchVector('position_type')).filter(search='Part-time').order_by('-date_posted')
            elif position_query == _('Volunteer'):
                qs = qs.annotate(search=SearchVector('position_type')).filter(search='Volunteer').order_by('-date_posted')
            elif position_query == _('Full-time'):
                qs = qs.annotate(search=SearchVector('position_type')).filter(search='Full-time').order_by('-date_posted')
            else:
                # handle the error that occurs from language toggling immediately after doing a search 
                return redirect('job-list')
    

    # paginate
    paginator = Paginator(qs, 20) # controls the # of ads per page
    page = request.GET.get('page')
    qs = paginator.get_page(page)

    context = {
        'ads': qs,
        'carousel_images': carousel_images,
        'keyword_query': keyword_query,
        'salary_query': salary_query,
        'location_query': location_query,
        'position_query': position_query,
        'location_list': location_list,
    }
    
    return render(request, 'classifieds/job_list.html', context)


class JobDetailView(DetailView):
    model = Job
    context_object_name = 'ad'


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    template_name = 'classifieds/job_update_form.html'
    context_object_name = 'ad'

    fields = [
        'title',
        'main_image',
        'image_2',
        'image_3',
        'title_of_position',
        'position_type',
        'experience',
        'degree_required',
        'salary',
        'location',
        'involves_travel',
        'company_name',
        'skype_id',
        'company_website',
        'job_description',
        ]

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ad = self.get_object()
        if self.request.user == ad.author:
            return True
        return False

    def get_success_url(self): 
        """
        After updating ad, provide success message and return to the detail view of associated ad.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your ad has been successfully updated!'))
        return reverse('job-list')


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'classifieds/job_confirm_delete.html'
    success_url = 'classifieds/job_update_form.html'
    context_object_name = 'ad'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self): 
        """
        After deleting ad, provide success message and return to the list of ads.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your ad has been successfully deleted!'))
        return reverse('job-list')


class SendEmailCreateView(CreateView):

    model = AdEmail
    form_class = SendEmailForm
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['ad'] = get_object_or_404(Ad, pk = self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        """
        Add author and associated ad to form data before setting it as valid (so it is saved to model)
        """
        # Associate logged-in user as author of email
        form.instance.author = self.request.user
        # Associate email with ad based on passed id
        form.instance.ad=get_object_or_404(Ad, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        to_email = form.instance.ad.author.email
        contact_email = self.request.user.email
        do_not_reply_msg = "**DO NOT REPLY to this email. To respond to the user, please use the email provided to you in their message. This is an automatic email server that serves only to put you in initial contact with users expressing interest in your ad, while keeping both your emails hidden to the public. Thank you!**"
        
        send_mail(
            '%s - %s is interested in your ad "%s"! (AUTOMATED EMAIL, DO NOT REPLY!)' % (title, self.request.user, form.instance.ad.title),
            '%s \n \nContact me at: %s \n \n%s' % (description, contact_email, do_not_reply_msg),
            'notifications@whattheblin.com',
            [to_email],
            fail_silently=False
            )

        return super().form_valid(form)

    def get_success_url(self): 
        """
        After posting comment, provide success message and return to associated blog post.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your email has been sent!'))
        return reverse('ad-list')


def FaqView(request):
    return render(request, 'classifieds/faq.html') 






    
    
