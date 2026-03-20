from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Members
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    members = Members.objects.all()
    
    return render(request, 'home.html', {'members':members})

def sign_in(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Get user by email
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("sign_in")

        # Authenticate using username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("base")  # Change to your dashboard URL name
        else:
            messages.error(request, "Invalid email or password")
            return redirect("sign_in")

    return render(request, "sign_in.html")

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "base.html")
