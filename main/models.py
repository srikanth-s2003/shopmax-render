from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_moified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=13, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
post_save.connect(create_profile, sender=User)
    
    
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length = 20)

    def __str__(self) -> str:
        return self.first_name
    
    
# class Picture(models.Model):
#     picture = models.ImageField(upload_to='products', blank=True)
#     def __str__(self):
#          return self.picture.url


class Product(models.Model):
    name = models.CharField(max_length=200)
    mrp = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    price = models.DecimalField(default=0, max_digits = 8, decimal_places = 2)
    Category = models.ForeignKey(Category, on_delete= models.CASCADE, default=1)
    description1 = models.CharField(max_length=100,default='', blank = True)
    description2 = models.CharField(max_length = 100,default='', blank = True)
    description3 = models.CharField(max_length = 100,default='', blank = True)
    description4 = models.CharField(max_length = 100,default='', blank = True)
    description5 = models.CharField(max_length = 100,default='', blank = True, null = True)
    mainDescription = models.TextField(default="", blank = True, null = True)
    # pictures = models.ForeignKey(Picture, blank=True,on_delete=models.CASCADE,related_name="product_img")
    images1 = models.ImageField(upload_to="products", default="", blank=True)
    images2 = models.ImageField(upload_to="products", default="", blank=True)
    images3 = models.ImageField(upload_to="products", default="", blank=True)
    images4 = models.ImageField(upload_to="products", default="", blank=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=20, default = '')
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default = False)

    def __str__(self) -> str:
        return f'{self.product}:shipped={self.status}'


class Banner(models.Model):
    title = models.CharField(max_length=200)
    sales = models.CharField(max_length=200)
    banner_img = models.ImageField(upload_to="banner")


    