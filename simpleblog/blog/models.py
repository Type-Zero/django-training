from django.db import models


class ArticleQuerySet(models.QuerySet):
    """
    Custom QuerySet for Blog Article model
    """
    def published(self):
        return self.filter(published=True)


class Article(models.Model):
    """
    Model for Blog Article.
    """
    title = models.CharField(max_length=90)
    body = models.TextField()
    slug = models.SlugField(max_length=90, unique=True)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = ArticleQuerySet.as_manager()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Blog Article'
        verbose_name_plural = 'Blog Articles'
        ordering = ['-created']