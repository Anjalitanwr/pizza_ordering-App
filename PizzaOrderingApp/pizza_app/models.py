from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    pizza_type = models.CharField(max_length=100)
    quantity = models.IntegerField(
        validators=[
            MaxValueValidator(70, message="Quantity cannot exceed 70."),
            MinValueValidator(1, message="Quantity must be at least 1.")
        ]
    )   
    
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"{self.customer_name} - {self.pizza_type} ({self.quantity})"