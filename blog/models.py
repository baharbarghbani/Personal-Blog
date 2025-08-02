from django.db import models

# Create your models here.
class Post(models.Model):
    def __str__ (self):
        return self.post_title
    post_title = models.CharField(max_length=20, default="Post")
    post_preview = models.CharField(max_length=200, default="Preview")
    content = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) # needs edit
