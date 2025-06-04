
import stripe
from unicodedata import category
import os


class Phones(models.Model):
    name=models.CharField(max_length=200)
    slug= models.CharField(max_length=255, unique=True, blank=True)
    brand = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    stripe_id = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    