from django.shortcuts import render
from django.http import HttpResponse
from . models import Members

# Create your views here.
def home(request):
    # members = Members.objects.get(id = pk)
    members = Members.objects.all()

    output = ""
    for member in members:
        output += f"{member.full_name} - {member.email}<br>"

    return HttpResponse(output)

