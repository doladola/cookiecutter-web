from django.db import models


class ServiceProbe(models.Model):
    slug = models.SlugField(unique=True)
    label = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.label
