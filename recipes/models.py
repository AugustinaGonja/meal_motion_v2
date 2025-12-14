from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(
        'Category', blank=True, related_name='recipes'
    )
    serving_size = models.CharField(max_length=50, blank=True)
    ingredients = models.JSONField()
    nutritional_value = models.JSONField()
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField('image', null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    instructions = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
