from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    # defines fields for profile objects
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        """Used to display username in profile page"""
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """After the model gets saved, use exisiting function and ensure resizing"""
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        