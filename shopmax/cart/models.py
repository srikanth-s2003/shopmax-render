from django.db import models

# Create your models here.
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.coupon_code