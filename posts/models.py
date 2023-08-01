from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Posts(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked', through='Like')

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']