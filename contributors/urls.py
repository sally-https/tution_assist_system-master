from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.contributorDashboard, name='contributorDashboard'),
    path('profile/', views.contributorProfile, name='contributorProfile'),
    # path('my_orders/', views.my_orders, name='customer_my_orders'),
    # path('order_detail/<int:order_number>/', views.order_detail, name='order_detail'),
]