from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Order, OrderItem
from .forms import ProductForm, OrderForm
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'home.html')

def is_admin(user):
    return user.is_staff

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'auth/iniciar_sesion.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'auth/iniciar_sesion.html', {
                'form': AuthenticationForm(),
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('home')
      
def signup(request):
    if request.method == 'GET':
        return render(request, 'auth/signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],  
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)  
                return redirect('home')  
            except IntegrityError:
                return render(request, 'auth/signup.html', {
                    'error': 'El usuario ya existe, elige otro.'
                })
        else:
            return render(request, 'auth/signup.html', {
                'error': 'Las contraseñas no coinciden.'
            })
        
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    order_items = [
        {
            'product': item.product,
            'quantity': item.quantity,
            'total_price': item.product.price * item.quantity  # Calcular el total del producto
        }
        for item in order.items.all()
    ]
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'orders/order_detail.html', context)

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    for item in items:
        item.subtotal = item.product.price * item.quantity
    total = sum(item.subtotal for item in items)
    return render(request, 'cart/cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if created:
        item.quantity = 1  
        item.save()
    else:
        item.quantity += 1
        if item.quantity > item.product.stock:
            item.quantity = item.product.stock  
        item.save()
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        if quantity > item.product.stock:
            quantity = item.product.stock
        item.quantity = quantity
        item.save()
    return redirect('cart')


@login_required
def place_order(request):
    items = CartItem.objects.filter(user=request.user)
    if not items:
        return redirect('product_list')
    order = Order.objects.create(user=request.user)
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        item.product.stock -= item.quantity
        item.product.save()
    items.delete()
    return redirect('order_confirmation', order_id=order.id)

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart')

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total_price)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()
    return redirect('user_orders')

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/user_order_list.html', {
        'orders': orders
    })

@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    orders = Order.objects.all()
    forms = {order.id: OrderForm(instance=order) for order in orders}
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
        return redirect('admin_orders')
    return render(request, 'orders/admin_order_list.html', {
        'orders': orders,
        'forms': forms
    })