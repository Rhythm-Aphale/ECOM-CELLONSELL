from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product

# Create your views here.\


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products_in_cart()
        quantities = cart.get_quantities() 
        total_price = cart.get_total_price()
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}, {my_shipping['shipping_state']} {my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = total_price
        
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save() 


            order_id = create_order.id

            for product in cart_products:
                product_id = product.id

                if product.is_sale:
                    price = product.sale_price

                else:
                    price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        quantity = int(value.get('quantity', 0))
                        create_order_item = OrderItem(order=create_order, product=product, user=user, quantity=quantity, price=price)
                        create_order_item.save()




            messages.success(request, 'Order Processed Successfully')   
            return redirect('home')

        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.id

            for product in cart_products:
                product_id = product.id

                if product.is_sale:
                    price = product.sale_price

                else:
                    price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        quantity = int(value.get('quantity', 0))
                        create_order_item = OrderItem(order=create_order, product=product, quantity=quantity, price=price)
                        create_order_item.save()





            messages.success(request, 'Order Processed Successfully')   
            return redirect('home')
    
    else:
        messages.success(request, 'Request Denied')
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products_in_cart()
        quantities = cart.get_quantities() 
        total_price = cart.get_total_price()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #check to see user logged in
        if request.user.is_authenticated:
            billing_form = PaymentForm(request.POST)
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "total_price": total_price, "shipping_info": request.POST, "billing_form": billing_form})
        else:
            #not logged in
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "total_price": total_price, "shipping_info": request.POST, "billing_form": PaymentForm()})


        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "total_price": total_price, "shipping_form": shipping_form})
    else:
        messages.success(request, 'Request Denied')
        return redirect('home')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products_in_cart()
    quantities = cart.get_quantities() 
    total_price = cart.get_total_price()
    shipping_form = ShippingForm(request.POST or None)
    
    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user=request.user)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            pass  # User doesn't have a shipping address yet, form will be empty
    
    return render(request, 'payment/checkout.html', {
        "cart_products": cart_products,
        "quantities": quantities,
        "total_price": total_price,
        "shipping_form": shipping_form
    })

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})






