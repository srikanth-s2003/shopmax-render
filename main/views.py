from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product, Profile, Category
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
import json
from cart.cart import Cart
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q 
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch
from django.http import JsonResponse

# Create your views here.
@cache_page(60 * 15)  # Cache for 15 minutes
def home(request):
    products = Product.objects.select_related('Category').all()[:12]  # Limit to 12 products for homepage
    category = Category.objects.prefetch_related('products').all()
    return render(request, 'index.html', {'products': products, 'productcat':category})

@cache_page(60 * 60)  # Cache for 1 hour
def about(request):
    return render(request, 'about.html', {})

def single(request, id):
    single_product = get_object_or_404(Product.objects.select_related('Category'), pk=id)
    return render(request, 'singlePage2.html',{'product':single_product})

def shop(request):
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')
    page = request.GET.get('page', 1)

    if order == 'desc':
        sort_by = '-' + sort_by

    items = Product.objects.select_related('Category').all().order_by(sort_by)
    
    # Add pagination
    paginator = Paginator(items, 12)  # Show 12 products per page
    products = paginator.get_page(page)
    
    return render(request, 'shop.html', {
        'products': products,
        'sort_by': sort_by.strip('-'),
        'order': order
    })

def shop_category(request, ctr):
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')   
    page = request.GET.get('page', 1)

    if order == 'desc':
        sort_by = '-' + sort_by

    # Convert URL-friendly format back to category name
    ctr = ctr.replace('-', ' ').title()
    
    try:
        # Case-insensitive category lookup
        category = Category.objects.get(name__iexact=ctr)
        products_list = Product.objects.select_related('Category').filter(Category=category).order_by(sort_by)
        
        # Add pagination
        paginator = Paginator(products_list, 12)
        products = paginator.get_page(page)
        
        return render(request, 'category.html', {
            'products': products,
            'category': category,
            'sort_by': sort_by.strip('-'),
            'order': order
        })
    except Category.DoesNotExist:
        # Get all available categories for debugging
        available_categories = list(Category.objects.values_list('name', flat=True))
        messages.warning(request, f"Category '{ctr}' not found. Available categories: {', '.join(available_categories)}")
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
    query = request.POST.get('q', '') if request.method == 'POST' else request.GET.get('q', '')
    query = query.strip()
    products = []
    
    if query:
        # Split query into words for better matching
        words = query.split()
        q_objects = Q()
        
        # Build query for each word
        for word in words:
            q_objects |= (
                Q(name__icontains=word) |
                Q(mainDescription__icontains=word)
            )
        
        # Get products matching any of the words, ordered by relevance
        products = Product.objects.filter(q_objects).select_related('Category').distinct()
        
        # Boost exact matches to top
        exact_matches = products.filter(name__icontains=query)
        if exact_matches.exists():
            # Move exact matches to the front
            products = list(exact_matches) + list(products.exclude(id__in=exact_matches.values_list('id', flat=True)))
    
    return render(request, 'search.html', {
        'products': products,
        'query': query,
        'total_results': len(products)
    })

def search_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '').strip().lower()
        
        if len(query) >= 2:  # Only search if 2 or more characters
            # First try exact matches from start of name
            exact_matches = Product.objects.filter(
                name__istartswith=query
            ).values_list('name', flat=True)[:3]
            
            # Then get contains matches, excluding exact matches
            contains_matches = Product.objects.filter(
                name__icontains=query
            ).exclude(
                name__in=exact_matches
            ).values_list('name', flat=True)[:3]
            
            # Combine results, prioritizing exact matches
            suggestions = list(exact_matches) + list(contains_matches)
            
            return JsonResponse({'suggestions': suggestions})
        return JsonResponse({'suggestions': []})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    social_account = user.socialaccount_set.first()
    
    if request.method == 'POST':
        # Update profile information
        profile.phone = request.POST.get('phone', '')
        profile.address1 = request.POST.get('address1', '')
        profile.address2 = request.POST.get('address2', '')
        profile.city = request.POST.get('city', '')
        profile.zipcode = request.POST.get('zipcode', '')
        profile.country = request.POST.get('country', '')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'user': user,
        'profile': profile,
        'email': user.email,
        'is_google_user': bool(social_account),
    }
    
    if social_account:
        extra_data = social_account.extra_data
        context.update({
            'profile_picture': extra_data.get('picture'),
            'given_name': extra_data.get('given_name'),
            'family_name': extra_data.get('family_name'),
            'locale': extra_data.get('locale'),
        })
    
    return render(request, 'profile.html', context)
    
