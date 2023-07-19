from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError


class CustomUserModel(AbstractUser):
    def save(self, *args, **kwargs):
        if not self.email:
            raise ValidationError('force required an email')

        super().save(*args, **kwargs)


class IconList(models.Model):
    name = models.TextField()
    color = models.CharField(blank=False, max_length=15, choices=(
        (' ', 'None'),
        ('text-primary', 'primary'),
        ('text-secondary', 'secondary'),
        ('text-success', 'success'),
        ('text-danger', 'danger'),
        ('text-warning', 'warning'),
        ('text-info', 'info'),
        ('text-light', 'light'),
        ('text-dark', 'dark'),
        ('text-muted', 'muted'),
        ('text-white', 'white'),
        ('link-primary', 'l-primary'),
        ('link-secondary', 'l-secondary'),
        ('link-success', 'l-success'),
        ('link-danger', 'l-danger'),
        ('link-warning', 'l-warning'),
        ('link-info', 'l-info'),
        ('link-light', 'l-light'),
        ('link-dark', 'l-dark'),
        ('link-muted', 'l-muted'),
        ('link-white', 'l-white'),

    ))
    icon = models.TextField()
    priority = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract = True

