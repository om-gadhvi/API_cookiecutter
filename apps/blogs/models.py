from django.db import models

class Blog(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_body = models.TextField(max_length=150)
    
    def __str__(self):
        return self.blog_title
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=50) 
    
    def __str__(self):
        return self.comment