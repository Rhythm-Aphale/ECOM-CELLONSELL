from django.shortcuts import render,redirect
from .models import Product,Cateogary,Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, userInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart




def search(request):
    #determine if the filled that form
    if request.method == "POST":
        searched = request.POST['searched']
        searched=Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        #contain is case sensitive and icontains is not case insensitive
        #test for null
        if not searched:
            messages.success(request, ("NO RESULTS FOUND"))
            return render(request, 'search.html', {}) 
        else:
            return render(request, 'search.html', {'searched':searched})
    else:
     return render(request, 'search.html', {})


def update_info(request):
    if request.user.is_authenticated:
        current_user = request.user
        try:
            shipping_user = ShippingAddress.objects.get(user=current_user)
        except ShippingAddress.DoesNotExist:
            shipping_user = None
        
        form = userInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your information has been updated successfully.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, "Please login first.")
        return redirect('home')



def update_password(request):
    if request.user.is_authenticated:
        current_user =  request.user

        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("YOU HAVE UPDATED YOUR PASSWORD SUCCESSFULLY"))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})   
        
    else:
        messages.success(request, ("PLEASE LOGIN FIRST"))
        return redirect('home')
   


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ("YOU HAVE UPDATED YOUR PROFILE SUCCESSFULLY"))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, ("PLEASE LOGIN FIRST"))
        return redirect('home')

def cateogary_summary(request, foo):
    # Your view logic here
    cateogary = Cateogary.objects.all()
    return render(request, 'cateogary_summary.html', {'cateogary':cateogary})


def cateogary(request,foo):
    foo = foo.replace('-', ' ')
    #GRAB THE CATEGORY FROM URL.PY FILE
    try:
        #LOOK UP THE CATEGORY
        cateogary = Cateogary.objects.get(name=foo)
        products = Product.objects.filter(cateogary=cateogary)
        return render(request, 'cateogary.html', {'products':products, 'cateogary':cateogary})

    
    except:
        messages.success(request, ("THAT CATEGORY DOESN'T EXIST"))
        return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render (request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render (request, 'home.html', {'products':products})

def about(request):
    return render (request, 'about.html', )



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            # Get saved cart from database
            saved_cart = current_user.old_cart
            # Convert database string to Python dictionary
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary
                cart = Cart(request)
                # Loop through the cart and add the items to the cart
                for key, value in converted_cart.items():
                    try:
                        # Retrieve the product object from the database using the product ID
                        product = Product.objects.get(id=key)
                        # Add the product to the cart
                        cart.add(product=product, quantity=value['quantity'])
                    except Product.DoesNotExist:
                        # Handle the case where the product does not exist
                        pass

            messages.success(request, ("YOU HAVE BEEN LOGGED IN SUCCESSFULLY....")) 
            return redirect('home')
        else:
            messages.success(request, ("THERE WAS AN ERROR PLEASE TRY")) 
            return redirect('login')
    else:
        return render(request, 'login.html', {})




def logout_user(request):
    logout(request)
    messages.success(request, ("YOU HAVE BEEN LOGOUT SUCCESSFULLY......"))
    return redirect('home' )



def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "USERNAME CREATED... PLEASE FILL THE USER INFO!")
                return redirect('update_info')
            else:
                messages.error(request, "WHOOPS! THERE WAS A PROBLEM REGISTERING")
                return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})



    