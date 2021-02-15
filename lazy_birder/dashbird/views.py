from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# this is a function based view, have to render the request
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'dashbird/home.html', context)


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


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

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

