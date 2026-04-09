from django.urls import path
from members import views
from .views import search_view

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.sign_in, name='sign_in'),
    path('register/', views.sign_up, name='sign_up'),
    path('add_member/', views.add_member, name='add_member'),
    path('finance/', views.finance, name='finance'),
    path('add_finance/', views.add_finance, name='add_finance'),
    path('finance_details/<uuid:uuid>/', views.finance_details, name='finance_details'),
    path('edit_finance/<uuid:uuid>/', views.edit_finance, name='edit_finance'),
    path('delete_finance/<uuid:uuid>/', views.delete_finance, name='delete_finance'),
    path('members/', views.members, name='members'),
    path('member_details/<uuid:uuid>/', views.member_details, name='member_details'),
    path('edit_member/<uuid:uuid>/', views.edit_member, name='edit_member'),
    path('delete_member/<uuid:uuid>/', views.delete_member, name='delete_member'),
    path('search/', search_view, name='search'),
    path('attendance/', views.attendance, name='attendance'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
]
