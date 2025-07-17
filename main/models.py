from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    mrp = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description1 = models.CharField(max_length=100, default='', blank=True)
    description2 = models.CharField(max_length=100, default='', blank=True)
    description3 = models.CharField(max_length=100, default='', blank=True)
    description4 = models.CharField(max_length=100, default='', blank=True)
    description5 = models.CharField(max_length=100, default='', blank=True, null=True)
    mainDescription = models.TextField(default="", blank=True, null=True)
    images1 = models.ImageField(upload_to="products", default="", blank=True)
    images2 = models.ImageField(upload_to="products", default="", blank=True)
    images3 = models.ImageField(upload_to="products", default="", blank=True)
    images4 = models.ImageField(upload_to="products", default="", blank=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.BooleanField(default=False)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address1 = models.TextField(blank=True)
    address2 = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=6, blank=True)
    country = models.CharField(max_length=100, default='')
    old_cart = models.TextField(blank=True, null=True, default='{}')
    date_moified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User) 


    