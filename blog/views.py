from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
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
    Post,
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
    BlogType,
    Tag,
    CarouselImage,
    FoodSearchBanner,
    LifeBlogSearchBanner,
    AboutUsBanner,
    FoodMap
)

from django.contrib.auth.models import User
from django.contrib import messages



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 27

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carousel'] = CarouselImage.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post

    # Add comments related to each food blog post to its context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(Post, pk = self.kwargs['pk'])
        # query comments, filter those related to the post
        comments_query = Comment.objects.all().order_by('-date_posted')
        comments_query_filtered = comments_query.filter(post_id=context['post'])
        context['user_comments'] = comments_query_filtered
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'card_image',
        'title',
        'overall_rating',
        'card_content',
        'banner',
        'the_good',
        'the_bad',
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
        'recommendation_write_up'
        ]

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
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
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    qs = AboutUsPicture.objects.all()
    banner = AboutUsBanner.objects.all()

    context = {
        'qs': qs,
        'banner': banner
    }
    return render(request, 'blog/about.html', context)


def valid_query(param):
    # makes sure that there is actually a search value and that it is not an empty string
    return param != '' and param is not None


def PostFilter(request):
    # query all post objects and feature objects
    qs = Post.objects.all()
    banner = FoodSearchBanner.objects.all()
    store_type = StoreType.objects.all()
    nearest_station = Station.objects.all()
    special_feature = SpecialFeature.objects.all()
    overall_rating = OverallRating.objects.all()
    taste_rating = TasteRating.objects.all()
    appearance_rating = AppearanceRating.objects.all()
    atmosphere_rating = AtmosphereRating.objects.all()
    price_rating = PriceRating.objects.all()
    service_rating = ServiceRating.objects.all()

    # retreive the form request
    title_query = request.GET.get('title')
    store_type_query = request.GET.get('store_type')
    nearest_station_query = request.GET.get('nearest_station')
    special_feature_query = request.GET.get('special_feature')
    overall_rating_query = request.GET.get('overall_rating')
    taste_rating_query = request.GET.get('taste_rating')
    appearance_rating_query = request.GET.get('appearance_rating')
    atmosphere_rating_query = request.GET.get('atmosphere_rating')
    price_rating_query = request.GET.get('price_rating')
    service_rating_query = request.GET.get('service_rating')
 
    # retrieve the form request queries for the life blogs
    if valid_query(title_query):
        qs = qs.filter(title__icontains=title_query)

    if valid_query(store_type_query) and store_type_query != 'Type...':
        qs = qs.filter(store_type__name=store_type_query)
    
    if valid_query(nearest_station_query) and nearest_station_query != 'Station...':
        qs = qs.filter(nearest_station__name=nearest_station_query)

    if valid_query(special_feature_query) and special_feature_query != 'Has...':
        qs = qs.filter(special_feature__name=special_feature_query)
        
    if valid_query(overall_rating_query) and overall_rating_query != 'Rating ≥ ...':
        qs = qs.filter(overall_rating__rating__gte=overall_rating_query).order_by('-overall_rating')

    if valid_query(taste_rating_query) and taste_rating_query != 'At least...':
        qs = qs.filter(taste_rating__rating__gte=taste_rating_query).order_by('-taste_rating')
    
    if valid_query(appearance_rating_query) and appearance_rating_query != 'At least...':
        qs = qs.filter(appearance_rating__rating__gte=appearance_rating_query).order_by('-appearance_rating')
    
    if valid_query(atmosphere_rating_query) and atmosphere_rating_query != 'At least...':
        qs = qs.filter(atmosphere_rating__rating__gte=atmosphere_rating_query).order_by('-atmosphere_rating')
    
    if valid_query(price_rating_query) and price_rating_query != 'Price...':
        qs = qs.filter(price_rating__name=price_rating_query)

    if valid_query(service_rating_query) and service_rating_query != 'At least...':
        qs = qs.filter(service_rating__rating__gte=service_rating_query).order_by('-service_rating')

    # paginate settings
    paginator = Paginator(qs, 27) # Show 27 blogs per page
    page = request.GET.get('page')
    qs = paginator.get_page(page)

    context = {
        'queryset': qs,
        'banner': banner,
        'title_query': title_query,
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
        'service_rating': service_rating
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
        context['post'] = get_object_or_404(Post, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form, *args, **kwargs):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.post=get_object_or_404(Post, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super().form_valid(form)

        
    def get_success_url(self): 
        """
        After posting comment, provide success message and return to associated blog post.
        """
        messages.add_message(self.request, messages.SUCCESS, 'Your comment has been successfully posted!')
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk'],})


class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(Post, pk = self.kwargs['pk'])
        return context



    """
    Form for adding a food blog comment. Requires login. 
    """
    model = LifeBlogComment
    fields = ['comment']
    context_object_name = 'comments'
    template_name = 'blog/life_blog_comment_form.html'

    def get_context_data(self, **kwargs):
        """
        Add associated life blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(LifeBlog, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form, *args, **kwargs):
        """
        Add author and associated life blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.post=get_object_or_404(LifeBlog, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super().form_valid(form)

        
    def get_success_url(self): 
        """
        After posting comment, provide success message and return to associated life blog post.
        """
        messages.add_message(self.request, messages.SUCCESS, 'Your comment has been successfully posted!')
        return reverse('life-blog-detail', kwargs={'pk': self.kwargs['pk'],})


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



    
class LifeBlogListView(ListView):
    model = LifeBlog
    template_name = 'blog/life.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 27


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
        messages.add_message(self.request, messages.SUCCESS, 'Your comment has been successfully posted!')
        return reverse('life-blog-detail', kwargs={'pk': self.kwargs['pk'],})


def LifeBlogFilter(request):
    # query all life post objects and blog types
    qs = LifeBlog.objects.all()
    banner = LifeBlogSearchBanner.objects.all()
    blog_type = BlogType.objects.all()
    tags = Tag.objects.all()
    

    # retreive the form request
    title_query = request.GET.get('title')
    blog_type_query = request.GET.get('blog_type')
    tags_query = request.GET.get('tags')


    # retrieve the form request queries for the life blogs
    if valid_query(title_query):
        qs = qs.filter(title__icontains=title_query)

    if valid_query(blog_type_query) and blog_type_query != 'Category...':
        qs = qs.filter(blog_type__name=blog_type_query)

    if valid_query(tags_query) and tags_query != 'Tags...':
        qs = qs.filter(tags__name=tags_query)

    # paginate
    paginator = Paginator(qs, 27) # Show 1 blogs per page
    page = request.GET.get('page')
    qs = paginator.get_page(page)

    context = {
        'queryset': qs,
        'title_query': title_query,
        'blog_type': blog_type,
        'blog_type_query': blog_type_query,
        'tags': tags,
        'tags_query': tags_query,
        'banner': banner,
    }

    return render(request, 'blog/life_search.html', context)