from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Members
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    # members = Members.objects.all()
    # return render(request, 'home.html', {'members':members})
    return render(request, 'home.html')

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
            return redirect("dashboard")  # Change to your dashboard URL name
        else:
            messages.error(request, "Invalid email or password")
            return redirect("sign_in")

    return render(request, "sign_in.html")

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("sign_up")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("sign_up")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("sign_up")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()
        print("USERNAME:", username)
        print("EMAIL:", email)

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("sign_in")

    return render(request, "sign_up.html")


@login_required
def dashboard(request):
    return render(request, "index.html")
