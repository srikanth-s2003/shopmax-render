from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .cart import Cart
from main.models import Product
from .models import Coupon
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
import uuid

@login_required
def summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    subtotal = cart.cart_total()
    total = subtotal
    return render(request, 'cart.html', {
        "cart_products": cart_products,
        "subtotal": subtotal,
        "total": total
    })

@login_required
def cart_add(request):
    if request.method == "POST" and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product=product)
        quantity = cart.__len__()
        return JsonResponse({"qty": quantity})
    return redirect('summary')

@login_required
def cart_delete(request):
    if request.method == "POST" and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart = Cart(request)
        cart.delete(product=product_id)
        messages.success(request, "Item Deleted From Shopping Cart.")
        return JsonResponse({'product': product_id})
    return redirect('summary')

@login_required
def checkout(request):
    cart = Cart(request)
    total_sub = 0

    if request.method == "POST":
        code = request.POST.get('coupon', '')
        try:
            coupon = Coupon.objects.get(coupon_code=code)
            total_sub = coupon.price
            messages.success(request, "Coupon code applied successfully.")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code.")

    cart_products = cart.get_prods
    subtotal = cart.cart_total()
    total = subtotal - total_sub
    return render(request, 'checkout.html', {
        "cart_products": cart_products,
        "subtotal": subtotal,
        "total": total
    })

# @login_required
# def thankyou(request):
#     cart = Cart(request)
#     cart_products = cart.get_prods
#     subtotal = cart.cart_total()
#     total = subtotal  # Apply coupon discount logic if needed
#     order_number = uuid.uuid4().hex[:10].upper()

#     subject = 'ORDER CONFIRMED'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = ["nimalashankar080@gmail.com"]


#     print(email_from, recipient_list, "------------------")

#     message = render_to_string('email.html', {
#         'name': request.user.username,
#         'products': cart_products,
#         'subtotal': int(subtotal),
#         'total': int(total),
#         'order_number': order_number
#     })

#     try:
#         email = EmailMessage(subject, message, email_from, recipient_list)
#         email.content_subtype = 'html'
#         email.fail_silently = False
#         email.send()
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Failed to send email: {e}")

#     return render(request, 'thankyou.html', {
#         'order_number': order_number,
#         'total': total
#     })

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from allauth.socialaccount.models import SocialAccount

@login_required
def thankyou(request):
    try:
        social_account = SocialAccount.objects.get(user=request.user)
        print(social_account.extra_data)  # Check what data is returned here
        if 'email' in social_account.extra_data:
            user_email = social_account.extra_data['email']
        else:
            user_email = None
            print("Email not found in extra_data")
    except SocialAccount.DoesNotExist:
        user_email = None

    cart = Cart(request)
    cart_products = cart.get_prods
    subtotal = cart.cart_total()
    total = subtotal
    order_number = uuid.uuid4().hex[:10].upper()

    subject = "ORDER CONFIRMED"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email] if user_email else []

    message = render_to_string("email.html", {
        "name": request.user.username,
        "products": cart_products,
        "subtotal": int(subtotal),
        "total": int(total),
        "order_number": order_number
    })

    try:
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.content_subtype = "html"
        email.send(fail_silently=False)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

    return render(request, "thankyou.html", {
        "order_number": order_number,
        "total": total
    })
