'''from email.policy import default
from inspect import _Object
from random import choices'''

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
            .filter(status='published')


class Postagem(models.Model):
    STATUS_CHOICES = (
        ['draft', 'Draft'],
        ['published', 'Published'],
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    # pubished = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    objects = models.Manager()  # Gerenciador default
    published = PublishedManager()  # gerenciador personalizado

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


posts = Postagem.published.all()
