from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('add/', views.add_skill, name='add_skill'),
    path('logout/', views.logout_user, name='logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('premium/', views.premium, name='premium'),

    path("pay/", views.khalti_payment, name="khalti_payment"),
    path("payment-success/", views.payment_success, name="payment_success"),

    path("dashboard/", views.admin_dashboard, name="dashboard"),
    path("swap/<int:skill_id>/", views.request_swap, name="request_swap"),
   path('userDashboard/', views.userDashboard, name='userDashboard'),

path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
path('reject/<int:request_id>/', views.reject_request, name='reject_request'),

path("dashboard/", views.admin_dashboard, name="dashboard"),

path("dashboard/users/", views.admin_users, name="admin_users"),
path("dashboard/skills/", views.admin_skills, name="admin_skills"),
path("dashboard/swaps/", views.admin_swaps, name="admin_swaps"),
path("dashboard/premium/", views.admin_premium, name="admin_premium"),
path("dashboard/payments/", views.admin_payments, name="admin_payments"),
path("dashboard/reports/", views.admin_reports, name="admin_reports"),
path("dashboard/settings/", views.admin_settings, name="admin_settings"),
]