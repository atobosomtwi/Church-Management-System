from django.urls import path
from members import views
# from .views import sign_in

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.sign_in, name='sign_in'),
    path('register/', views.sign_up, name='sign_up'),
]
