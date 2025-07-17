from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('shop/', views.shop, name="shop"),
    path('shop/<str:ctr>/', views.shop_category, name="shop_category"),
    path('search/', views.search, name="search"),
    path('search/ajax/', views.search_ajax, name="search_ajax"),
    path('product/<int:id>', views.single, name="single_product"),
    path('login_user/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)