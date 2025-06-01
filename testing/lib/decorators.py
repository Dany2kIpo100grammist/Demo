from django.shortcuts import redirect
from django.urls import reverse

def login_required_redirect(view_func):
    def wrapped_view(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))
        
        return view_func(request, *args, **kwargs)
    return wrapped_view