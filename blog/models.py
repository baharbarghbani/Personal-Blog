from django.db import models

# Create your models here.
class Post(models.Model):
    def __str__ (self):
        return self.post_title
    post_title = models.CharField(max_length=100, default="Post")  
    post_preview = models.CharField(max_length=500, default="Preview")  
    content = models.TextField(default="Content")  
    date_posted = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) # needs edit

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.post_title, self.name)