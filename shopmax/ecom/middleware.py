# myapp/middleware.py
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

class ExtendSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            max_age = timedelta(seconds=settings.SESSION_COOKIE_AGE)
            expiry_age = timezone.now() + max_age
            request.session.set_expiry(expiry_age)
        
        return response
