from django import forms
from .models import Product, Order, OrderItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

# Formulario para ítems de pedido
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
