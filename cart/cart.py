from store.models import Product,Profile
from django.contrib.sessions.models import Session
from json import dumps

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.cart = self.session.get('cart', {})

    def db_add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += product_qty  # Add to existing quantity
        else:
            self.cart[product_id] = {'quantity': product_qty}  # Add new item

        self.save()

        if self.request.user.is_authenticated:
            try:
                current_user_profile = Profile.objects.get(user=self.request.user)
                current_user_profile.old_cart = dumps(self.cart)
                current_user_profile.save()
            except Profile.DoesNotExist:
                # Profile does not exist for the user, create one
                current_user_profile = Profile.objects.create(user=self.request.user, old_cart=dumps(self.cart))
                current_user_profile.save()

    


        

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += product_qty  # Add to existing quantity
        else:
            self.cart[product_id] = {'quantity': product_qty}  # Add new item

        self.save()

        if self.request.user.is_authenticated:
            try:
                current_user_profile = Profile.objects.get(user=self.request.user)
                current_user_profile.old_cart = dumps(self.cart)
                current_user_profile.save()
            except Profile.DoesNotExist:
                # Profile does not exist for the user, create one
                current_user_profile = Profile.objects.create(user=self.request.user, old_cart=dumps(self.cart))
                current_user_profile.save()

 



    def get_total_price(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total_price = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total_price += product.sale_price * value['quantity']
                    else:

                        total_price += product.price * value['quantity']
    
        return total_price


    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def __len__(self):
        return sum(item.get('quantity', 0) for item in self.cart.values())

    def get_products_in_cart(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quantities(self):
        return self.cart

    

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
    
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_qty
        else:
        # If product not in cart, you may choose to handle it as you see fit,
        # such as raising an error or adding it to the cart
            pass

        self.session.modified = True
        if self.request.user.is_authenticated:
            try:
                current_user_profile = Profile.objects.get(user=self.request.user)
                current_user_profile.old_cart = dumps(self.cart)
                current_user_profile.save()
            except Profile.DoesNotExist:
                # Profile does not exist for the user, create one
                current_user_profile = Profile.objects.create(user=self.request.user, old_cart=dumps(self.cart))
                current_user_profile.save()

        return self.cart
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
        else:
            raise Product.DoesNotExist
        if self.request.user.is_authenticated:
            try:
                current_user_profile = Profile.objects.get(user=self.request.user)
                current_user_profile.old_cart = dumps(self.cart)
                current_user_profile.save()
            except Profile.DoesNotExist:
                # Profile does not exist for the user, create one
                current_user_profile = Profile.objects.create(user=self.request.user, old_cart=dumps(self.cart))
                current_user_profile.save()

  
        
    
        

    
        
            


    




