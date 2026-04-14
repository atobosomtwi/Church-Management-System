from django.contrib import admin
from . models import Members, UserProfiles, Finance,Attendance, Visitors
# testing

class MembersAdmin(admin.ModelAdmin):
    #display data in a tabular form on the django admin page.
    list_display = ['full_name', 'email', 'phone_number', 'location', 'dob','gender', 'date_registered']
    search_fields = ('full_name', 'location')
    list_filter = ['gender', 'date_registered']
# Register your models here.

class UserProfilesAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'profile']

admin.site.register(UserProfiles, UserProfilesAdmin)
admin.site.register(Members, MembersAdmin)


# Changing Admin Site name 
admin.site.site_title = "Apostolic church"
admin.site.site_header = "Apostolic church Portal"
admin.site.index_title = "Welcome to Apostolic church"


@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ("date_created", "purpose", "type", "amount", "uuid")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("date", "recorded_by", "service_type", "non_registered", "member")


@admin.register(Visitors)
class VisitorsAdmin(admin.ModelAdmin):
    list_display = ('full_name','gender', 'phone_number', 'location', 'service_type' , 'date_registered')
    search_fields = ('full_name', 'phone_number')
    list_filter = ['gender', 'date_registered']


# @admin.register()
# class Admin(admin.ModelAdmin):
#     list_display = ("")



