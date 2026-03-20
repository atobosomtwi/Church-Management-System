from django.contrib import admin
from . models import Members
# testing

class MembersAdmin(admin.ModelAdmin):
    #display data in a tabular form on the django admin page.
    list_display = ['full_name', 'email', 'phone_number', 'location', 'dob','gender', 'date_registered']
    search_fields = ('full_name', 'location')
    list_filter = ['gender', 'date_registered']
# Register your models here.
admin.site.register(Members, MembersAdmin)

# Changing Admin Site name 
admin.site.site_title = "Apostolic church"
admin.site.site_header = "Apostolic church Portal"
admin.site.index_title = "Welcome to Apostolic church"
