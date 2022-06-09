from django.db import models
from django.contrib.auth.models import User
from model_utils import FieldTracker


# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    product = models.CharField(max_length=2000, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    old_price = models.IntegerField(null=True, blank=True)
    wishPrice = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    
    tracker = FieldTracker(fields=['price'])
    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']