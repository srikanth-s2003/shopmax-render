
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap


sitemaps = {
    'static': StaticViewSitemap,  # 'static' is the key, and the value is the sitemap class
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls')),
    path('cart/', include('cart.urls')),

    # google url
    # path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
