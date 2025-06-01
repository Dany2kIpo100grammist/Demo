from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth

from user.forms import LoginForm, RegisterForm, MakeRequestForm
from lib.decorators import login_required_redirect

from app import settings

# Create your views here.

# Компонент логина
def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = auth.authenticate(username=username, password=password)
            
            if user:
                auth.login(request, user)
                
                if user.is_superuser: return redirect('/admin/')
    else:
        form = LoginForm()
    
    context = {
        "form": form,
        "exception_fields": (),
    }
    
    return render(request, "login.html", context)

# Компонент регистрации
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        
        print(request.POST.get("password1"))
        
        if form.is_valid():
            # commit=False чтобы можно было сделать промежуточные проверки
            # commit=True чтобы можно под березой найти говно и т.д
            user = form.save(commit=False)
            
            # Тут можно ебануть промежуточные проверки
            user.password2 = request.POST.get("password1")

            user.save()
            auth.login(request, user)
            
            return redirect("main:index")
    else:
        form = RegisterForm()
    
    context = {
        "form": form,
        "exception_fields": ("password2"),
    }
    
    return render(request, "register.html", context)

@login_required_redirect
def requests_view(request):
    if request.method == "POST":
        form = MakeRequestForm(data=request.POST)
        
        if form.is_valid():
            instance = form.save(commit=False)
            
            # Тут можно ебануть промежуточные проверки
            instance.user = request.user
            if instance.isCustom:
                instance.service = form.cleaned_data.get("customService")
            else:
                instance.service = settings.SERVICE_TYPES[instance.service]
            
            instance.save()
            
            return redirect(reverse("main:index"))
    else:
        form = MakeRequestForm()
    
    context = {
        "form": form,
        "exception_fields": (),
    }
    
    return render(request, "requests.html", context)

@login_required_redirect
def requests_history_view(request):
    requests = request.user.requests.all()
    
    print(requests)
    
    context = {
        "requests": requests
    }
    
    return render(request, "requestsHistory.html", context)