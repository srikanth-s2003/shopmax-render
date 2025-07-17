from django.contrib import admin
from . import models
from django.contrib.auth.models import User


# Register your models here.
# admin.site.register(models.Customer)
admin.site.register(models.Category)
admin.site.register(models.Product)
# admin.site.register(models.Picture)
admin.site.register(models.Order)
admin.site.register(models.Profile)


# mix profile info user
class ProfileInline(admin.StackedInline):
    model = models.Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    # fields = ['__all__']
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)


