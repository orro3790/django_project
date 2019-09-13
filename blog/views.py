from django.shortcuts import render, render_to_response, get_object_or_404, reverse, HttpResponseRedirect, HttpResponse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import (
    FoodBlog,
    StoreType,
    Station,
    SpecialFeature,
    OverallRating,
    TasteRating,
    AppearanceRating,
    AtmosphereRating,
    PriceRating,
    ServiceRating,
    Comment,
    LifeBlogComment,
    AboutUsPicture,
    LifeBlog,
    BlogCategory,
    Tag,
    CarouselImage,
    FoodSearchBanner,
    LifeBlogSearchBanner,
    AboutUsBanner,
    FoodMap,
    Profile,
    # Russian models
    RussianBlogCategory,
    RussianTag,
    RussianStoreType,
    RussianStation,
    RussianSpecialFeature,
    RussianPriceRating
)

from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.postgres import search
from django.contrib.postgres.search import SearchVector


def FoodBlogListView(request):

    carousel_images = CarouselImage.objects.all()
    template_name = 'blog/home.html'

    language = get_language()
    
    if language == "en":
        posts = FoodBlog.objects.all()

    if language == "ru":
        posts = FoodBlog.objects.all().filter(publish_translated_blog=True)
    
    # paginate settings
    paginator = Paginator(posts, 1) # Show # blogs per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'carousel_images': carousel_images
    }
    
    return render(request, 'blog/home.html', context)
    

class PostDetailView(DetailView):
    model = FoodBlog

    # Add comments related to each food blog post to its context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(FoodBlog, pk = self.kwargs['pk'])
        comments_query = Comment.objects.all().order_by('-date_posted')
        comments_query_filtered = comments_query.filter(post_id=context['post'])
        context['user_comments'] = comments_query_filtered
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FoodBlog
    fields = [
        'card_image',
        'title',
        'overall_rating',
        'card_content',
        'the_good',
        'the_bad',
        'banner',
        'paragraph_1',
        'snapshot_1',
        'paragraph_2',
        'snapshot_2',
        'paragraph_3',
        'snapshot_3',
        'paragraph_4',
        'snapshot_4',
        'paragraph_5',
        'snapshot_5',
        'store_type',
        'nearest_station',
        'taste_rating',
        'appearance_rating',
        'atmosphere_rating',
        'service_rating',
        'price_rating',
        'special_feature',
        'google_map',
        'dish_recommendation',
        'recommendation_write_up',
        'date_posted',
        'author'
        ]

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FoodBlog
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    qs = AboutUsPicture.objects.all()
    banner = AboutUsBanner.objects.all()
    matt = User.objects.get(username='Matt')
    steph = User.objects.get(username='Steph')

    context = {
        'qs': qs,
        'banner': banner,
        'matt': matt,
        'steph': steph
    }
    return render(request, 'blog/about.html', context)


def valid_query(param):
    # makes sure that there is actually a search value and that it is not an empty string
    return param != '' and param is not None


def FoodBlogFilter(request):

    # Query all life post objects
    carousel_image = FoodSearchBanner.objects.all()
    store_type = StoreType.objects.all()
    nearest_station = Station.objects.all()
    special_feature = SpecialFeature.objects.all()
    overall_rating = OverallRating.objects.all()
    taste_rating = TasteRating.objects.all()
    appearance_rating = AppearanceRating.objects.all()
    atmosphere_rating = AtmosphereRating.objects.all()
    price_rating = PriceRating.objects.all()
    service_rating = ServiceRating.objects.all()
    store_type_russian = RussianStoreType.objects.all()
    nearest_station_russian = RussianStation.objects.all()
    special_feature_russian = RussianSpecialFeature.objects.all()
    price_rating_russian = RussianPriceRating.objects.all()

    # retreive the form request
    keyword_query = request.GET.get('title')
    store_type_query = request.GET.get('store_type')
    nearest_station_query = request.GET.get('nearest_station')
    special_feature_query = request.GET.get('special_feature')
    overall_rating_query = request.GET.get('overall_rating')
    price_rating_query = request.GET.get('price_rating')

    # check the language settings of the user
    language = get_language()
    
    if language == "en":

        qs = FoodBlog.objects.all()

        if valid_query(keyword_query):
            qs = LifeBlog.objects.annotate(search=SearchVector('title', 'paragraph_1'),).filter(search='Cheese')

        if valid_query(store_type_query) and store_type_query != 'Type...' and store_type_query != 'Тип...':
            qs = qs.filter(store_type__name=store_type_query)
        
        if valid_query(nearest_station_query) and nearest_station_query != 'Station...' and nearest_station_query != 'Станция...':
            qs = qs.filter(nearest_station__name=nearest_station_query)

        if valid_query(special_feature_query) and special_feature_query != 'Features...' and special_feature_query != 'Характеристики...':
            qs = qs.filter(special_feature__name=special_feature_query)
            
        if valid_query(overall_rating_query) and overall_rating_query != 'Rating ≥ ...' and overall_rating_query != 'Рейтинг ≥ ...':
            qs = qs.filter(overall_rating__rating__gte=overall_rating_query)

        if valid_query(price_rating_query) and price_rating_query != 'Price...' and price_rating_query != 'Цена...':
            qs = qs.filter(price_rating__name=price_rating_query)
    
    if language == "ru":

        qs = FoodBlog.objects.all().filter(publish_translated_blog=True)

        if valid_query(keyword_query):
            qs = qs.filter(title_russian__icontains=keyword_query)

        if (valid_query(store_type_query) and store_type_query != 'Тип...' and store_type_query != 'Type...'):
            qs = qs.filter(store_type_russian__name=store_type_query)

        if valid_query(nearest_station_query) and nearest_station_query != 'Станция...' and nearest_station_query != 'Station...':
            qs = qs.filter(nearest_station_russian__name=nearest_station_query)

        if valid_query(special_feature_query) and special_feature_query != 'Характеристики...' and special_feature_query != 'Features...':
            qs = qs.filter(special_feature_russian__name=special_feature_query)

        if valid_query(overall_rating_query) and overall_rating_query != 'Рейтинг ≥ ...' and overall_rating_query != 'Rating ≥ ...':
            qs = qs.filter(overall_rating__rating__gte=overall_rating_query)

        if valid_query(price_rating_query) and price_rating_query != 'Цена...' and price_rating_query != 'Price...':
            qs = qs.filter(price_rating_russian__name=price_rating_query)
        

    # paginate settings
    paginator = Paginator(qs, 1) # Show 27 blogs per page
    page = request.GET.get('page')
    qs = paginator.get_page(page)

    context = {
        'queryset': qs,
        'carousel_images': carousel_image,
        'keyword_query': keyword_query,
        'store_type': store_type,
        'store_type_query': store_type_query,
        'nearest_station': nearest_station,
        'nearest_station_query': nearest_station_query,
        'special_feature': special_feature,
        'special_feature_query': special_feature_query,
        'overall_rating': overall_rating,
        'overall_rating_query': overall_rating_query,
        'taste_rating': taste_rating,
        'appearance_rating': appearance_rating,
        'atmosphere_rating': atmosphere_rating,
        'price_rating': price_rating,
        'price_rating_query': price_rating_query,
        'service_rating': service_rating,
        'store_type_russian': store_type_russian,
        'special_feature_russian': special_feature_russian,
        'nearest_station_russian': nearest_station_russian,
        'price_rating_russian': price_rating_russian,
    }

    return render(request, 'blog/search.html', context)


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Form for adding a food blog comment. Requires login. 
    """
    model = Comment
    fields = ['comment']
    context_object_name = 'comments'

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(FoodBlog, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form, *args, **kwargs):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.post=get_object_or_404(FoodBlog, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super().form_valid(form)

        
    def get_success_url(self): 
        """
        After posting comment, provide success message and return to associated blog post.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your comment has been successfully posted!'))
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk'],})


class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(FoodBlog, pk = self.kwargs['pk'])
        return context


class MapView(TemplateView):
    template_name = "blog/map.html"

    # Add map url context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Query the map model to grab the url
        map_query = FoodMap.objects.all()
        context['map'] = map_query
        return context


class LifeBlogDetailView(DetailView):
    model = LifeBlog
    template_name = 'blog/life_detail.html'
    context_object_name = 'post'

    # Add comments related to each life blog post to its context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(LifeBlog, pk = self.kwargs['pk'])
        # query comments, filter those related to the post
        comments_query = LifeBlogComment.objects.all().order_by('-date_posted')
        comments_query_filtered = comments_query.filter(post_id=context['post'])
        context['user_comments'] = comments_query_filtered
        return context


class LifeBlogCommentCreateView(LoginRequiredMixin, CreateView):
    """
    Form for adding a food blog comment. Requires login. 
    """
    model = LifeBlogComment
    fields = ['comment']
    context_object_name = 'comments'
    template_name = 'blog/life_blog_comment_form.html'

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(LifeBlog, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form, *args, **kwargs):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.post=get_object_or_404(LifeBlog, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super().form_valid(form)

        
    def get_success_url(self): 
        """
        After posting comment, provide success message and return to associated blog post.
        """
        messages.add_message(self.request, messages.SUCCESS, _('Your comment has been successfully posted!'))
        return reverse('life-blog-detail', kwargs={'pk': self.kwargs['pk'],})


def LifeBlogFilter(request):

    # Query all life post objects and blog types for logged-in users
    qs = LifeBlog.objects.all()
    carousel_image = LifeBlogSearchBanner.objects.all()
    blog_category = BlogCategory.objects.all()
    tags = Tag.objects.all()
    blog_category_russian = RussianBlogCategory.objects.all()
    tags_russian= RussianTag.objects.all()
    
    # retreive form requests
    keyword_query = request.GET.get('title')
    blog_category_query = request.GET.get('blog_category')
    tags_query = request.GET.get('tags')

    # check the language settings of the user
    language = get_language()

    # retrieve the English form request queries
    if language == 'en':
        if valid_query(keyword_query):
            qs = LifeBlog.objects.annotate(search=SearchVector('title', 'card_content', 'paragraph_1', 'paragraph_2', 'paragraph_3', 'paragraph_4', 'paragraph_5')).filter(search=keyword_query)

        if valid_query(blog_category_query) and blog_category_query != 'Category...':
            qs = qs.filter(blog_category__name=blog_category_query)

        if valid_query(tags_query) and tags_query != 'Tags...':
            qs = qs.filter(tags__name=tags_query)

    # retrieve the Russian form request queries
    if language == 'ru':
        qs = LifeBlog.objects.annotate(search=SearchVector('title', 'card_content', 'paragraph_1', 'paragraph_2', 'paragraph_3', 'paragraph_4', 'paragraph_5')).filter(search=keyword_query)

        if valid_query(blog_category_query) and blog_category_query != 'Категория...':
            qs = qs.filter(blog_category_russian__name=blog_category_query)

        if valid_query(tags_query) and tags_query != 'Теги...':
            qs = qs.filter(tags_russian__name=tags_query)


    # paginate
    paginator = Paginator(qs, 1) # Show 1 blogs per page
    page = request.GET.get('page')
    qs = paginator.get_page(page)

    context = {
        'queryset': qs,
        'keyword_query': keyword_query,
        'blog_category': blog_category,
        'blog_category_query': blog_category_query,
        'tags': tags,
        'tags_query': tags_query,
        'carousel_images': carousel_image,
        'blog_category_russian': blog_category_russian,
        'tags_russian': tags_russian,
    }

    return render(request, 'blog/life_search.html', context)