from django.db import models

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('home', 'Home Service'),
        ('business', 'Business Service'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    
    def __str__(self):
        return self.name
