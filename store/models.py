from django.contrib.sessions.models import Session
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#CATEGORIES OF PRODUCTS

class Cateogary(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

    class Meta:
        
        verbose_name_plural = 'Categories'


# create a customer profile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, default='', blank=True)
    address1 = models.CharField(max_length=200, default='', blank=True)
    address2 = models.CharField(max_length=200, default='', blank=True)
    city = models.CharField(max_length=50, default='', blank=True)
    state = models.CharField(max_length=50, default='', blank=True)
    zip = models.CharField(max_length=10, default='', blank=True)
    country = models.CharField(max_length=50, default='', blank=True)
    old_cart =models.CharField(max_length=1000, default='', blank=True, null=True)
   
    

    def __str__(self):
        return self.user.username

# create a user profile by default when user sign up

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)


#CUSTOMER
class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'



    
    


#all of our products
    

class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(default=0, decimal_places=2, max_digits=10)
    cateogary=models.ForeignKey(Cateogary, on_delete=models.CASCADE, default=1)
    description=models.CharField(max_length=250, default='', blank=True, null=True)
    image=models.ImageField(upload_to='uploads/product/')

    #ADD SALES ON WEBSITE

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=7)

    def __str__(self):
        return self.name





#customer order
class Order(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=200, default='', blank=True)
    phone=models.CharField(max_length=20, default='', blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)


    def __str__(self):
        return self.product
    
    class Meta:
        db_table = 'store_order' 

