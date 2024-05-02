from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product
from django.http import HttpRequest
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products_in_cart()  # Corrected method name
    quantities = cart.get_quantities() 
    total_price = cart.get_total_price()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "total_price": total_price})


def cart_add(request: HttpRequest):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        # Basic input validation
        if not product_id or not product_qty:
            return JsonResponse({'error': 'Invalid input'})

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'})

        try:
            product_qty = int(product_qty)
            if product_qty < 1:
                return JsonResponse({'error': 'Invalid quantity'})
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'})

        cart.add(product=product, quantity=product_qty)
        cart_quantity = len(cart)
        messages.success(request, ("PRODUCT ADDED TO CART SUCCESSFULLY...."))
        return JsonResponse({'qty': cart_quantity})
        
    else:
        return JsonResponse({'error': 'Invalid request'})



def cart_delete(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        cart = Cart(request)
        product_id = request.POST.get('product_id')

        if not product_id:
            return JsonResponse({'error': 'Invalid input'})

        try:
            cart.delete(product=product_id)
            messages.success(request, ("PRODUCT REMOVED FROM CART SUCCESSFULLY...."))   
            return JsonResponse({'success': 'Product removed from cart'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'})
    else:
        return JsonResponse({'error': 'Invalid request'})

    

def cart_update(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        if not product_id or not product_qty:
            return JsonResponse({'error': 'Invalid input'})

        try:
            product_qty = int(product_qty)
            cart.update(product=product_id, quantity=product_qty)
            messages.success(request, ("CART UPDATED SUCCESSFULLY...."))
            return JsonResponse({'success': 'Cart updated successfully'})
        except ValueError:
            return JsonResponse({'error': 'Invalid input'})
    else:
        return JsonResponse({'error': 'Invalid request'})







