from django.contrib.auth.models import AbstractUser
from django.db import models


STRAND_CHOICES = [
    ('HUMSS', 'HUMSS'),
    ('ABM', 'ABM'),
    ('TVL', 'TVL'),
    ('GAS', 'GAS'),
]


class User(AbstractUser):
    """Custom user model with strand."""
    STRAND_CHOICES = STRAND_CHOICES
    
    strand = models.CharField(
        max_length=10,
        choices=STRAND_CHOICES,
        default='GAS',
        help_text='Academic strand'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

