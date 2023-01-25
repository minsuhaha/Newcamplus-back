from django.db import models
from django.utils import timezone
from users.models import User


CATEGORY_CHOICES = (
    ('book', '책'),
    ('charger', '충전기'),
    ('calculator', '계산기'),
    ('student product', '학생용품'),
    ('lost item', '분실물'),
    ('etx', '그 외')
)


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=128)
    location = models.CharField(max_length=50, blank=True)
    category = models.CharField(
        max_length=40, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[4][0])
    body = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text
