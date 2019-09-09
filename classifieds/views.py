from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView
from . models import (
    Ad,
    Job,
    AdEmail,
    Buyer,
    Seller
)
from . forms import (
    AdForm,
    JobForm,
    SendEmailForm
)
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.postgres import search
from django.contrib.postgres.search import SearchVector


class AdCreateView(LoginRequiredMixin, CreateView):

    model = Ad
    form_class = AdForm

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self): 
        """
        After posting comment, provide success message and return to associated blog post.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your ad has been successfully posted!'))
        return reverse('ad-list')


def valid_query(param):
    # makes sure that there is actually a search value and that it is not an empty string
    return param != '' and param is not None


def AdListView(request):
    model = Ad
    template_name = 'classifieds/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-date_posted']
    all_ads = Ad.objects.all()

    contains_query = request.GET.get('contains_filter')
    category_query = request.GET.get('category_filter')
    # split the string value from the count and grab just the string itself:
    if category_query != None:
        category_query = request.GET.get('category_filter').split('-')[0]
        
    LANGUAGE_CODE = get_language()

    # English views
    # Outcome #1: default page load
    if category_query == None and contains_query == None:
        qs = all_ads

    # Outcome #2: a user presses search with no values
    if (category_query == 'Category...' and contains_query == '') or (category_query == 'Категория...' and contains_query == ''):
        qs = all_ads

    # Outcome #3: a user provides search values
    # Searching for "Contains...", user actually submits a value
    if valid_query(contains_query) and contains_query != "Contains..." and contains_query != "Название содержит...":
        qs = Ad.objects.annotate(search=SearchVector('title', 'description', 'items_or_model_names'),).filter(search=contains_query)


    # If a category is submitted, pull English their respective ads as well.
    if valid_query(category_query):

        if 'посуда и приборы' in category_query:
            qs = all_ads.filter(category__search='kitchenware and appliances').order_by('-date_posted')

        if 'искусства и ремесла' in category_query:
            qs = all_ads.filter(category__search='arts and crafts').order_by('-date_posted')

        if 'малыш и дети' in category_query:
            qs = all_ads.filter(category__search='baby and kids').order_by('-date_posted')

        if 'красота и здоровье' in category_query:
            qs = all_ads.filter(category__search='beauty and health').order_by('-date_posted')

        if 'велосипеды' in category_query:
            qs = all_ads.filter(category__search='bikes').order_by('-date_posted')

        if 'книги' in category_query:
            qs = all_ads.filter(category__search='books').order_by('-date_posted')

        if 'телефоны' in category_query:
            qs = all_ads.filter(category__search='cell phones').order_by('-date_posted')

        if 'одежда' in category_query:
            qs = all_ads.filter(category__search='clothing').order_by('-date_posted')

        if 'предметы коллекционирования' in category_query:
            qs = all_ads.filter(category__search='collectibles').order_by('-date_posted')

        if 'компьютеры' in category_query:
            qs = all_ads.filter(category__search='computers').order_by('-date_posted')
        
        if 'электроника' in category_query:
            qs = all_ads.filter(category__search='electronics').order_by('-date_posted')

        if 'сад' in category_query:
            qs = all_ads.filter(category__search='garden').order_by('-date_posted')

        if 'мебель' in category_query:
            qs = all_ads.filter(category__search='furniture').order_by('-date_posted')

        if 'свободно' in category_query:
            qs = all_ads.filter(category__search='free').order_by('-date_posted')
        
        if 'генеральный' in category_query:
            qs = all_ads.filter(category__search='general').order_by('-date_posted')

        if 'домашнее хозяйство' in category_query:
            qs = all_ads.filter(category__search='household').order_by('-date_posted')

        if 'домашнее животное' in category_query:
            qs = all_ads.filter(category__search='pets').order_by('-date_posted')
        
        if 'ювелирные изделия' in category_query:
            qs = all_ads.filter(category__search='jewelery').order_by('-date_posted')

        if 'материалы' in category_query:
            qs = all_ads.filter(category__search='materials').order_by('-date_posted')

        if 'музыкальные инструменты' in category_query:
            qs = all_ads.filter(category__search='musical instruments').order_by('-date_posted')

        if 'камеры' in category_query:
            qs = all_ads.filter(category__search='cameras').order_by('-date_posted')

        if 'инструменты' in category_query:
            qs = all_ads.filter(category__search='tools').order_by('-date_posted')

        if 'игры' in category_query:
            qs = all_ads.filter(category__search='games').order_by('-date_posted')   

    # paginate
    paginator = Paginator(qs, 30) # controls the # of objects per page
    page = request.GET.get('page')
    qs = paginator.get_page(page)

    context = {
        'ads': qs,
        'contains_query': contains_query,
        'category_query': category_query,
        'CODE': LANGUAGE_CODE
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
        'image_1',
        'image_2',
        'image_3',
        'items_or_model_names',
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
        return reverse('jobs-list')


def JobListView(request):
    model = Job
    template_name = 'classifieds/job_list.html'
    context_object_name = 'ads'
    ordering = ['-date_posted']
    full_qs = Job.objects.all().order_by('-date_posted')
    paginator_qs = Job.objects.all().order_by('-date_posted')
    paginator = Paginator(paginator_qs, 5) # controls the # of objects per page
    page = request.GET.get('page')
    qs = paginator.get_page(page)
    salary_query = request.GET.get('salary_filter')
    contains_query = request.GET.get('contains_filter')

    if valid_query(salary_query) and salary_query != 'Salary of at least...' and salary_query != 'Зарплата как минимум ...':
        # look for a match containing first 6 digits of query, because the embedded counts in the template get passed into the query also and interfere with the matching. 
        qs = full_qs.filter(salary__gte=salary_query[:6]).order_by('-date_posted')

    if valid_query(contains_query) and salary_query != 'Contains...':
        qs = full_qs.filter(title__icontains=contains_query).order_by('-date_posted')

    context = {
        'ads': qs,
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
        'image',
        'title_of_position',
        'experience',
        'position_type',
        'education',
        'salary',
        'location',
        'involves_travel',
        'name',
        'skype_id',
        'email',
        'company_website',
        'company_description',
        'job_description'
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
        return reverse('jobs-list')


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
        return reverse('jobs-list')


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






    
    
