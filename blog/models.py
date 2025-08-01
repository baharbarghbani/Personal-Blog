from django.db import models

# Create your models here.
class Post(models.Model):
    def __str__ (self):
        return self.name
    post_name = models.CharField(max_length=20, default="Post")
    post_preview = models.CharField(max_length=100, default="Preview")
    content = models.CharField(max_length=200)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) # needs edit
