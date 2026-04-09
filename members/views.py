from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . models import Members, Finance, Attendance
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
from django.utils import timezone


# Create your views here.
# @login_required(login_url='sign_in') #forces users to login before accessing the homepage.
# def home(request):
#     # members = Members.objects.all()
#     # return render(request, 'home.html', {'members':members})
#     return render(request, 'home.html')

@login_required(login_url='sign_in')
def dashboard(request):
    initials = request.user.username[0]
    members = Members.objects.all().order_by('-id')[:5]
    return render(request, "index.html", {"members": members, 'initials':initials})


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
def add_member(request):
    if request.method == "POST" or request.FILES:
        full_name = request.POST['full_name']
        gender = request.POST['gender']
        dob = request.POST['dob']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        picture = request.FILES.get('picture')
        is_baptized = request.POST['is_baptized']
        marital_status = request.POST['marital_status']
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
            marital_status = marital_status,
        )

        member.save()
        showAlert(request, 'Member added successfully', 'success')
    return render(request, 'add_member.html')

@login_required(login_url='sign_in')
def members(request):
    members = Members.objects.all().order_by('id')
    context = {
        'members': members,
        'total_members': Members.objects.all().count(),
        'baptized': Members.objects.filter(is_baptized=True).count(),
        'unbaptized': Members.objects.filter(is_baptized=False).count(),
        'singles': Members.objects.filter(marital_status='single').count(),
    }
    return render(request, 'members.html', context)

@login_required(login_url='sign_in')
def member_details(request, uuid):
    member = Members.objects.get(uuid=uuid)
    context = {
        'member': member
    }
    print(member.full_name)
    return render(request, 'member_details.html', context)

@login_required(login_url='sign_in')
def edit_member(request, uuid):
    member = Members.objects.get(uuid=uuid)
    if request.method == 'POST' or request.FILES:
        member.full_name = request.POST.get('full_name')
        member.email = request.POST.get('email')
        member.phone_number = request.POST.get('phone_number')
        member.location = request.POST.get('location')
        member.dob = request.POST.get('dob')
        member.gender = request.POST.get('gender')
        member.marital_status = request.POST.get('marital_status')
        member.is_baptized = True if request.POST.get('is_baptized') == "True" else False
        if request.FILES:
            member.picture = request.FILES['picture']
        member.save()
        showAlert(request, f"{member.full_name.split(' ')[0]} updated successfully", 'success')
        return redirect('members')
    
    context = {
        'member': member
    }

    return render(request, 'edit_member.html', context)

@login_required(login_url='sign_in')
def delete_member(request, uuid):
    # member = get_object_or_404(Members, uuid=uuid)
    member = Members.objects.get(uuid=uuid)
    member.delete()
    showAlert(request, f"{member.full_name.split(' ')} deleted successfully", 'success')
    return redirect('members')


def search_view(request):
    query = Members.objects.GET.get('q')  # get search input
    results = []

    if query:
        results = Members.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'results': results
    }
    return render(request, 'search_results.html', context)


@login_required(login_url='sign_in')
def finance(request):
    transactions = Finance.objects.all().order_by('id')
    total_income = 0
    total_expenditure = 0

    for income in Finance.objects.filter(type="Income"):
        total_income += income.amount

    for expense in Finance.objects.filter(type="Expense"):
        total_expenditure += expense.amount


    balance = total_income - total_expenditure
   
    context = {
        "transactions": transactions,
        "total_income": total_income,
        "total_expenditure": total_expenditure,
        "balance" : balance,
    }
    return render(request, 'finance.html', context)

@login_required(login_url='sign_in')
def add_finance(request):
    if request.method == "POST" or request.FILES:
        category = request.POST['category']
        type1 = request.POST['type1']
        purpose = request.POST['purpose']
        amount = request.POST['amount']
        # date_created = request.POST['date_created']
       

        transaction = Finance.objects.create(
            category = category,
            type = type1,
            purpose = purpose,
            amount = amount,
            # date_created = date_created,
           
        )
      
        transaction.save()
        showAlert(request, 'Transaction added successfully', 'success')
        return redirect('finance')
    return render(request, 'add_finance.html')

@login_required(login_url='sign_in')
def finance_details(request, uuid):
    transaction = Finance.objects.get(uuid=uuid)
    context = {
        'transaction': transaction
    }
    print(transaction.category)
    return render(request, 'finance_details.html', context)

@login_required(login_url='sign_in')
def edit_finance(request, uuid):
    transaction = Finance.objects.get(uuid=uuid)
    if request.method == 'POST':
        transaction.category = request.POST.get('category')
        transaction.type = request.POST.get('type')
        transaction.purpose = request.POST.get('purpose')
        transaction.amount = request.POST.get('amount')
        # transaction.date_created = request.POST.get('date_created')
        
        transaction.save()
        showAlert(request, f"{transaction.category} updated successfully", 'success')
        return redirect('finance')
    
    context = {
        'transaction': transaction
    }

    return render(request, 'edit_finance.html', context)

@login_required(login_url='sign_in')
def delete_finance(request, uuid):
    # member = get_object_or_404(Members, uuid=uuid)
    transaction = Finance.objects.get(uuid=uuid)
    transaction.delete()
    showAlert(request, f"{transaction.category} deleted successfully", 'success')
    return redirect('finance')



@login_required(login_url='sign_in')
def attendance(request):
    attendance_records = Attendance.objects.all()
    sunday_attendance = attendance_records.filter(service_type='sunday')
    midweek_attendance = attendance_records.filter(service_type='midweek')
    members = Members.objects.all().order_by('-full_name')

    context = {
        "sunday_attendance":sunday_attendance,
        "midweek_attendance":midweek_attendance,
        "attendance_records":attendance_records,
        "members":members,
    }


    return render(request, 'attendance.html', context)


@login_required(login_url='sign_in')
def mark_attendance(request):
    if request.method == "POST":
        member_id =  request.POST['member_id']
        service_type =  request.POST['service_type']
        member = Members.objects.get(uuid=member_id)
        today = timezone.now().date()
        date = Attendance.objects.filter(member=member, date__date = today)
        if date:
            showAlert(request, "Attendance already recorded", "warning")
        else:
            attendance = Attendance.objects.create(
                member = member,
                service_type = service_type,
                recorded_by = f"{request.user} -- {request.user.id}"
            )
            attendance.save()
            showAlert(request, "Attendance recorded", "success")
        return redirect('attendance')


