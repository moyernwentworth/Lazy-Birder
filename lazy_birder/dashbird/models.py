from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    bird_photo = models.ImageField(default='media/default.jpg')

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        # this gives the address to be sent to after a user creates a post
        return reverse('post-detail', kwargs={'pk': self.pk})