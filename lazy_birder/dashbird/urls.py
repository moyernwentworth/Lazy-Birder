from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostUpdateView, 
    PostDeleteView, 
    UserPostListView
)
from . import views

urlpatterns = [
    # calling a class as a view
    path('', views.home, name='dashbird-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # calling a function as a view
    path('bird-posts/', views.bird_posts, name='bird-posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete')
]