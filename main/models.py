import uuid
from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
    ('ball', 'Balls'),
    ('shoes', 'Shoes'),
    ('jersey', 'Jersey'),
    ('armband', 'Armband'),
    ('others', 'Others'),
]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)  # FIXED: added max_length
    thumbnail = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_hot = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.name