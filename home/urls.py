from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    # Skills
    path('add/', views.add_skill, name='add_skill'),
    path('swap/<int:skill_id>/', views.request_swap, name='request_swap'),

    # User Dashboard
    path('userDashboard/', views.userDashboard, name='userDashboard'),

    # Swap Request Actions
    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),

    # Chat
    path('chat/<int:swap_id>/', views.chat, name='chat'),

    # Chatbot
    path('chatbot/', views.chatbot, name='chatbot'),

    # Premium & Payment
    path('premium/', views.premium, name='premium'),
    path('pay/', views.khalti_payment, name='khalti_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),

    # ===============================
    # Admin Dashboard
    # ===============================

    path('dashboard/', views.admin_dashboard, name='dashboard'),

    path('dashboard/users/', views.admin_users, name='admin_users'),
    path('dashboard/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    path('dashboard/skills/', views.admin_skills, name='admin_skills'),
    path('dashboard/swaps/', views.admin_swaps, name='admin_swaps'),
    path('dashboard/premium/', views.admin_premium, name='admin_premium'),
    path('dashboard/payments/', views.admin_payments, name='admin_payments'),
    path('dashboard/reports/', views.admin_reports, name='admin_reports'),
    path('dashboard/settings/', views.admin_settings, name='admin_settings'),
path(
    "dashboard/skills/delete/<int:skill_id>/",
    views.delete_skill,
    name="delete_skill"
),
path(
    "dashboard/swaps/delete/<int:swap_id>/",
    views.delete_swap,
    name="delete_swap"
),
path(
    "dashboard/premium/",
    views.admin_premium,
    name="admin_premium"
),

path(
    "dashboard/premium/remove/<int:profile_id>/",
    views.remove_premium,
    name="remove_premium"
),

]