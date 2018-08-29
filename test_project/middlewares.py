import re

from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from django.shortcuts import redirect, reverse




class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        path = request.path
        if request.session.get('user', None):
            if path == reverse('login') or path == reverse('registration'):
                return redirect('index')
        else:
            if path == reverse('index')\
                    or path == reverse('dashboard')\
                    or path == reverse('profile')\
                    or path == reverse('users')\
                    or path == reverse('groups'):

                return redirect('login')
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response