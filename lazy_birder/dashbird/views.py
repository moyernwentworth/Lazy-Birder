from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# this is a function based view, have to render the request
def home(request):
    current_user = request.user
    automated_post = Post(
            title = 'Test Post',
            author = current_user,
            content = 'This is an example post',
            date_posted = datetime.now(),
            bird_photo = 'media/test1.jpeg'
        )
    automated_post.save()
    post_list =  Post.objects.filter(author=current_user).order_by('-date_posted')
    # if we want to show all users posts
    # post_list = Post.objects.all().order_by('-date_posted')
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 5)
    try: 
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # context = {
    #     'posts': Post.objects.all()
    # }
    return render(request, 'dashbird/home.html', {'posts': posts})


def about(request):
    return render(request, 'dashbird/about.html', {'title': 'About'})


# this is a class based view
class PostListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    template_name = 'dashbird/home.html'
    context_object_name = 'posts'
    # posts go from most recent on the top
    ordering = ['-date_posted']
    # set number of posts per page
    paginate_by = 5

    def automate_posts(self, request):
        automated_post = Post(
            title = 'Test Post',
            author = self.request.user,
            content = 'This is an example post',
            date_posted = datetime.now(),
            bird_photo = 'media/test1.jpeg'
        )
        automated_post.save()



class UserPostListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    template_name = 'dashbird/user_posts.html'
    context_object_name = 'posts'
    # set number of posts per page
    paginate_by = 5


    def get_queryset(self):
        """filter posts by user, show them reverse chronologically"""
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

        

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'bird_photo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'bird_photo']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        return True if self.request.user == post.author else False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'


    def test_func(self):
        """ensures the logged in user is editing their own post, no one elses"""
        post = self.get_object()
        return True if self.request.user == post.author else False

