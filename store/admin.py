from django.contrib import admin
from .models import Cateogary,Customer,Product,Order,Profile
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Cateogary)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)



#mix profile with user

class ProfileInline(admin.StackedInline):
    model = Profile
    

#extend user model

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [ProfileInline]

#unregister user model
admin.site.unregister(User)

#register user model with new UserAdmin
admin.site.register(User, UserAdmin)