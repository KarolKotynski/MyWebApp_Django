from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from meme_site.models import MemePost

# Create your models here.

class About_me(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=50)

class MySiteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="incognito.png", upload_to="Profile_image")

    def __str__(self):
        return f"{self.user.username} Profie."
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)