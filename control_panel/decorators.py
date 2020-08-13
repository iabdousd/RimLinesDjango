from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_required(view_function):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_function(request, *args, **kwargs)
    return wrapper_func


def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                groups = request.user.groups.all()
                for group in groups:
                    for role in allowed_roles:
                        if group.name == role:
                            return view_func(request, *args, **kwargs)
            return HttpResponse("403")
        return wrapper_func
    return decorator
