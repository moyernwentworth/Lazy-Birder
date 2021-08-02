from django.urls import path
from .views import (
    PostDetailView, 
    PostUpdateView, 
    PostDeleteView, 
    UserPostListView
)
from . import views

# defines url extensions for the site
urlpatterns = [
    path('', views.home, name='dashbird-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('bird-posts/', views.bird_posts, name='bird-posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete')
]