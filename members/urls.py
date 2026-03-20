from django.urls import path
from members import views
# from .views import sign_in

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.sign_in, name='sign_in')
]
