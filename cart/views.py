from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from .cart import Cart
from django.contrib import messages
from main.models import Product, Order
from .models import Coupon
from django.core.mail import send_mail, EmailMessage
from  django.template.loader import render_to_string
from django.conf import settings 
from django.contrib.auth.decorators import login_required


def summary(request):
    if request.user.is_authenticated:
        total_sub = 0  # Initialize total_sub to 0

        # if request.method == "POST":
        #     code = request.POST.get('coupon', '')  # Use get method to safely retrieve 'coupon' from POST data
        #     try:
        #         coupon = Coupon.objects.get(coupon_code=code)
        #         total_sub = coupon.price  # Use the price of the retrieved coupon
        #         print(total_sub)
        #         messages.success(request, "Coupon code applied successfully")
        #     except Coupon.DoesNotExist:
        #         messages.success(request, "Coupon code is invalid.")  
        #     # return render(request, 'cart.html')
        
        cart = Cart(request)
        cart_products = cart.get_prods
        subtotal = cart.cart_total()
        total = subtotal - total_sub  # Subtract the coupon price from the total
        # print(total, "\n\n\n\n\n")
        return render(request, 'cart.html', {"cart_products": cart_products, "total": total, "subtotal":subtotal})
    else:
         return redirect('/login_user/')


def cart_add(request):
    if request.user.is_authenticated:
        cart = Cart(request)

        if request.POST.get('action')=='post':
            product_id = int(request.POST.get('product_id'))
            # product_qty = int(request.POST.get('qty'))
            # print(product_id)
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product)

            quantity = cart.__len__()
            response = JsonResponse({"qty":quantity})
            return response
    else:
        return redirect('/login_user/')

         
    
def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
		cart.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response
    

def checkout(request):
    if request.user.is_authenticated:
        total_sub = 0  # Initialize total_sub to 0

        if request.method == "POST":
            code = request.POST.get('coupon', '')  # Use get method to safely retrieve 'coupon' from POST data
            try:
                coupon = Coupon.objects.get(coupon_code=code)
                total_sub = coupon.price  # Use the price of the retrieved coupon
                # print(total_sub)
                messages.success(request, "Coupon code applied successfully")
            except Coupon.DoesNotExist:
                messages.success(request, "Coupon code is invalid.")  
            # return render(request, 'cart.html')
        
        cart = Cart(request)
        cart_products = cart.get_prods
        subtotal = cart.cart_total()
        total = subtotal - total_sub  # Subtract the coupon price from the total
        return render(request, 'checkout.html', {"cart_products": cart_products, "total": total, "subtotal":subtotal})
    else:
         return redirect('/login_user/')
    
    # return render(request, 'checkout.html')

def thankyou(request):

    
    total_sub = 0  # Initialize total_sub to 0

    cart = Cart(request)
    cart_products = cart.get_prods
    subtotal = cart.cart_total()
    total = subtotal - total_sub
    order_number = 10011


    subject = 'ORDER CONFIRMED'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email,]

    message = render_to_string('email.html', {
         'name':request.user,
         'products':cart_products,
         'subtotal':int(subtotal),
         'total':int(total),
         'order_number':order_number
         })
    
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.fail_silently = True
    email.content_subtype = 'html'
    email.send()
        
    send_mail(subject, message, 'ShopMax <email_from>', recipient_list)
    return render(request, 'thankyou.html', {})

