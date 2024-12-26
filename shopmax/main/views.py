from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product, Banner, Profile, Category
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
import json
from cart.cart import Cart
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q 


# Create your views here.
def home(request):
    # return HttpResponse('<h1>hello bro</h1>')
    products = Product.objects.all()
    category = Category.objects.all()
    # print(category)
    # for cat in category:
    #     print(cat)
    banner = Banner.objects.get(pk=1)
    return render(request, 'index.html', {'products': products, 'banner': banner, 'productcat':category})

def about(request):
    return render(request, 'about.html', {})

def single(request, id):
    single_product  = Product.objects.get(pk=id)
    return render(request, 'singlePage2.html',{'product':single_product})




def shop(request):
    sort_by = request.GET.get('sort_by', 'name')  # Default sorting by name
    order = request.GET.get('order', 'asc')       # Default ordering is ascending

    if order == 'desc':
        sort_by = '-' + sort_by

    items = Product.objects.all().order_by(sort_by)
    return render(request, 'shop.html', {'products': items, 'sort_by': sort_by.strip('-'), 'order': order})
    # products = Product.objects.all()
    # return render(request, 'shop.html',{'products':products})

def shop_category(request, ctr):

    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')   

    if order == 'desc':
        sort_by = '-' + sort_by

    ctr = ctr.replace('-', ' ')
    try:
        category = Category.objects.get(name=ctr)
        products = Product.objects.filter(Category = category).order_by(sort_by)
        return render(request,'category.html', {'products':products})
    except:
        messages.warning(request, "Category not found..")
        return redirect('shop')



@csrf_protect
def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            username = User.objects.get(email=email.lower()).username
        except:
            print('------------------\n im here\n')
            username = ''
            pass

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
            
                converted_cart = json.loads(saved_cart)
                # add the loaded cart dictionary to session
                cart = Cart(request)
                # loop through the cart and add them to the session
                for key, value in converted_cart.items():
                    cart.db_add(product=key)

            return redirect('/')
        else:
            messages.error(request, "invalid credentials")
            return redirect('/')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "there was a error")
            return redirect('/register/')
    else:
        return render(request, 'register.html', {'form':form})
    

def search(request):
    if request.method == "POST":
        q1 = q2 = None
        searched = request.POST.get('q', '')
        print(searched)
        try:
            q1, q2 = searched.split()
        except:
            q1 = searched

        results = Product.objects.filter(Q(name__icontains=q1) | Q(mainDescription__icontains=searched))
        request.session['searched'] = searched  # Store the searched keyword in session
        return render(request, "shop.html", {'products': results})
    else:
        searched = request.session.get('searched', 'search')  # Retrieve the searched keyword from session
        print(searched)
        sort_by = request.GET.get('sort_by', 'name')  # Default sorting by name
        order = request.GET.get('order', 'asc')       # Default ordering is ascending

        if order == 'desc':
            sort_by = '-' + sort_by

        items = Product.objects.filter(Q(name__icontains=searched)).order_by(sort_by)
        return render(request, 'shop.html', {'products': items, 'sort_by': sort_by.strip('-'), 'order': order})


def profile(request):
    name = request.user
    email = request.user.email
    return render(request, 'profile.html', {'name':name, 'email':email})
    
