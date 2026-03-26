from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Members
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . utils import showAlert
# -----
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# ----------

# Create your views here.
@login_required(login_url='sign_in') #forces users to login before accessing the homepage.
def home(request):
    # members = Members.objects.all()
    # return render(request, 'home.html', {'members':members})
    return render(request, 'home.html')

def sign_in(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_obj = User.objects.filter(email=email)
        # Authenticate using username and password
        user = authenticate(request, username=user_obj.first().username if user_obj else " ", password=password)

        if user is not None:
            login(request, user)
            showAlert(request, "logged in successfull",'success')
            return redirect("dashboard")  # Change to your dashboard URL name
        else:
            showAlert(request, "Invalid email or password",'danger')
            return redirect("sign_in")

    return render(request, "sign_in.html")





def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check empty fields
        if not username or not email or not password:
            showAlert(request, "All fields are required", 'danger')
            return redirect("sign_up")

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            showAlert(request, "Invalid email format", 'danger')
            return redirect("sign_up")

        # Password match
        if password != confirm_password:
            showAlert(request, "Passwords do not match", 'danger')
            return redirect("sign_up")

        # Check duplicates
        if User.objects.filter(username=username).exists():
            showAlert(request, "Username already exists", 'danger')
            return redirect("sign_up")

        if User.objects.filter(email=email).exists():
            showAlert(request, "Email already registered", 'danger')
            return redirect("sign_up")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()
        showAlert(request, "Account created successfully. Please log in.", 'success')
        return redirect("sign_in")

    return render(request, "sign_up.html")


@login_required(login_url='sign_in')
def dashboard(request):
    members = Members.objects.all().order_by('-id')[:5]
    return render(request, "index.html", {"members": members})

def add_member(request):
    if request.method == "POST" or request.FILES:
        full_name = request.POST['full_name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        picture = request.FILES.get('picture')
        is_baptized = request.POST['is_baptized']
        location = request.POST['location']

        member = Members.objects.create(
            full_name = full_name,
            gender = gender,
            dob = dob,
            email = email,
            phone_number = phone_number,
            location = location,
            picture = picture,
            is_baptized = True if is_baptized == "True" else False,
        )

        member.save()
    return render(request, 'add_member.html')