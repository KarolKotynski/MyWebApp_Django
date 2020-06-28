from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.urls import reverse

# Create your models here.


class MemePost(models.Model):
    #slug = models.SlugField(unique=False, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='meme_images/', blank=False, null=False)
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now)
    thumb_up = models.ManyToManyField(User, related_name="liked_up", blank=True)
    thumb_down = models.ManyToManyField(User, related_name="liked_down", blank=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.user.username}, {self.title}"
    
    def get_absolute_url(self):
        return reverse('memeDetailView', kwargs={'id': self.id})
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 700 or img.width > 600:
            output_size = (700, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

# creating class Comment section:
# our post will be foreign key taken from MemePost
# user will be assigned to actual User
# content could be created with max length 500 characters
# timestamt will be actual time
class Comment_section(models.Model):
    post = models.ForeignKey(MemePost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(default=timezone.now)

    # creating printable class
    def __str__(self):
        return f"{self.post.title}, {self.user.username}"