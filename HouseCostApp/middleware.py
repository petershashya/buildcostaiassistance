# myapp/middleware.py

from django.shortcuts import redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            # User is not authenticated, check if they are accessing a protected page
            if request.path != '/login/' and not request.path.startswith('/accounts/login/'):
                return redirect('/login')
        else:
            # User is authenticated, ensure their session is active
            if request.session.get_expiry_age() <= 0:
                # Session has expired, log out the user and redirect to the login page
                from django.contrib.auth import logout
                logout(request)
                return redirect('/login')
