from main.models import Product, Profile
from django.contrib.auth.models import User

class Cart:
    def __init__(self, request):
        self.session = request.session

        self.request = request

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            

        self.cart = cart 

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True


    def db_add(self, product):
        product_id = str(product)
        # product_qty = int(product)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product)}
            # self.cart[product_id] = int(product)
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))
            

        
    def add(self, product):
        product_id = str(product.id)
        # product_qty = int(product)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}
            # self.cart[product_id] = int(product)
        self.session.modified = True

        if self.request.user.is_authenticated:
            
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))
            
    

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)

        quantities = self.cart

        total = 0
        for key in quantities.keys():
            
            key = int(key)
            for product in products:
                if product.id == key:
                    total = total+product.price
        return total
    
    def delete(self, product):
        product_id = str(product)
		# Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
			# Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        
        products = Product.objects.filter(id__in=product_ids)
        return products
