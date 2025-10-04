from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="FontAwesome or custom CSS icon class (e.g. 'fa fa-headset')"
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
