from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('SUPPLEMENTS', 'Suplementos'),
        ('EQUIPMENT', 'Equipo de gimnasio'),
        ('APPAREL', 'Ropa deportiva'),
        ('ACCESSORIES', 'Accesorios'),
    )
    name = models.CharField(max_length=200)  
    description = models.TextField(blank=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock = models.PositiveIntegerField()  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING') 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} (User: {self.user.username})'
    