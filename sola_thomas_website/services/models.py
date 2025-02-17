from django.db import models

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('home', 'Home Services'),
        ('business', 'Business Services'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
