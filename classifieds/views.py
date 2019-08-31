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
        messages.add_message(self.request, messages.SUCCESS, 'Your ad has been successfully posted!')
        return reverse('ad-list')


def valid_query(param):
    # makes sure that there is actually a search value and that it is not an empty string
    return param != '' and param is not None


def AdListView(request):
    model = Ad
    template_name = 'classifieds/ad_list.html'
    context_object_name = 'ads'
    ordering = ['-date_posted']
    full_qs = Ad.objects.all().order_by('-date_posted')
    paginator_qs = Ad.objects.all().order_by('-date_posted')
    paginator = Paginator(paginator_qs, 5) # controls the # of objects per page
    page = request.GET.get('page')
    qs = paginator.get_page(page)
    title_query = request.GET.get('title_filter')
    category_query = request.GET.get('category_filter')
    
    if valid_query(title_query) and title_query != "I'm looking for...":
        # display only top 100 most recent results if search is initiated
        qs = full_qs.filter(title__icontains=title_query).order_by('-date_posted')[:100]

    if valid_query(category_query) and category_query != "Category...":
        # look for a match containing first 4 letters of query, because the embedded counts in the template get passed into the query also and interfere with the matching. 
        # display only top 100 most recent results if search is initiated, 
        qs = full_qs.filter(category__contains=category_query[:4]).order_by('-date_posted')[:100]

    context = {
        'ads': qs,
        'full_qs': full_qs
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
        messages.add_message(self.request, messages.SUCCESS, 'Your ad has been successfully updated!')
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
        messages.add_message(self.request, messages.SUCCESS, 'Your ad has been successfully deleted!')
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
        messages.add_message(self.request, messages.SUCCESS, 'Your ad has been successfully posted!')
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
    title_query = request.GET.get('title_filter')

    if valid_query(salary_query) and salary_query != 'Salary of at least...':
        # look for a match containing first 6 digits of query, because the embedded counts in the template get passed into the query also and interfere with the matching. 
        qs = full_qs.filter(salary__gte=salary_query[:6]).order_by('-date_posted')[:100]

    if valid_query(title_query) and salary_query != 'Title contains...':
        qs = full_qs.filter(title__icontains=title_query).order_by('-date_posted')[:100]

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
        'company_description'
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
        messages.add_message(self.request, messages.SUCCESS, 'Your ad has been successfully updated!')
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
        messages.add_message(self.request, messages.SUCCESS, 'Your ad has been successfully deleted!')
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
        messages.add_message(self.request, messages.SUCCESS, 'Your email has been sent!')
        return reverse('ad-list')


def FaqView(request):
    return render(request, 'classifieds/faq.html') 






    
    
