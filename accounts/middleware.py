from django.shortcuts import redirect
from django.conf import settings
'''
class RedirectDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code in [301, 302]:
            print(f"REDIRECT TO: {response.get('Location')}")
        return response


# core/middleware.py
from django.shortcuts import redirect
from django.conf import settings
'''

class RedirectDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Проверяем, является ли ответ редиректом (301, 302, 303, 304, 305, 307, 308)
        if 300 <= response.status_code < 400:
            # --- СТАВЬТЕ BREAKPOINT НА ЭТОЙ СТРОКЕ ---
            location = response.get('Location', 'Unknown')
            print(f"DEBUG REDIRECT: {request.path} -> {location} (Status: {response.status_code})")

        return response
