from django.urls import path
from members import views

urlpatterns = [
    path('', views.home, name='home')
]
