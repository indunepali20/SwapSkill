from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill, Profile, SwapRequest

import json
import requests

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt



# HOME
def home(request):
    skills = Skill.objects.all()
    return render(request, 'home.html', {'skills': skills})


# CHATBOT
def chatbot(request):
    message = request.GET.get("message", "").lower()

    if "hello" in message:
        reply = "Hello 👋 Welcome to SwapSkill!"
    elif "skill" in message:
        reply = "You can add or learn skills from the platform 🚀"
    elif "login" in message:
        reply = "Go to login page to access your account 🔐"
    elif "register" in message:
        reply = "Register to start sharing skills 🧠"
    elif "payment" in message:
        reply = "Payment feature will be added soon 💰"
    else:
        reply = "Sorry, I didn’t understand."

    return JsonResponse({"reply": reply})


# PREMIUM PAGE
@login_required(login_url='/login/')
def premium(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.is_premium = True
        profile.save()

        messages.success(request, "Premium activated successfully 💎")
        return redirect('home')

    return render(request, 'premium.html', {'profile': profile})


# PAYMENT SUCCESS (FIXED ERROR WAS HERE)
@login_required(login_url='/login/')
def payment_success(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.is_premium = True
    profile.save()

    messages.success(request, "Payment successful 💎 You are now premium!")
    return redirect("home")


# REGISTER
def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html')


# LOGIN
def login_user(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# LOGOUT
def logout_user(request):
    logout(request)
    return redirect('login')


# ADD SKILL
@login_required(login_url='/login/')
def add_skill(request):
    if request.method == "POST":
        Skill.objects.create(
            user=request.user,
            skill_have=request.POST.get('skill_have'),
            skill_want=request.POST.get('skill_want'),
            description=request.POST.get('description')
        )
        return redirect('home')

    return render(request, 'add_skill.html')


# ADMIN DASHBOARD
@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('home')

    total_users = User.objects.count()
    total_skills = Skill.objects.count()
    total_premium = Profile.objects.filter(is_premium=True).count()

    recent_users = User.objects.all().order_by('-date_joined')[:5]
    recent_skills = Skill.objects.all().order_by('-id')[:5]

    return render(request, 'admin/dashboard.html', {
        'total_users': total_users,
        'total_skills': total_skills,
        'total_premium': total_premium,
        'recent_users': recent_users,
        'recent_skills': recent_skills,
    })

@csrf_exempt
@login_required
def khalti_payment(request):

    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=400)

    try:
        data = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        data = {}

    url = "https://dev.khalti.com/api/v2/epayment/initiate/"

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "return_url": "http://127.0.0.1:8000/payment-success/",
        "website_url": "http://127.0.0.1:8000/",
        "amount": 19900,
        "purchase_order_id": f"ORDER-{request.user.id}",
        "purchase_order_name": "Premium Membership",
        "customer_info": {
            "name": request.user.username,
            "email": request.user.email or "test@email.com",
            "phone": "9800000000"
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    return JsonResponse(response.json())

@login_required
def request_swap(request, skill_id):

    skill = Skill.objects.get(id=skill_id)

    if skill.user == request.user:
        messages.error(request, "You cannot request your own skill.")
        return redirect("home")

    already_requested = SwapRequest.objects.filter(
        sender=request.user,
        receiver=skill.user,
        skill=skill
    ).exists()

    if already_requested:
        messages.warning(request, "You already sent a request.")
        return redirect("home")

    SwapRequest.objects.create(
        sender=request.user,
        receiver=skill.user,
        skill=skill
    )

    messages.success(request, "Swap request sent successfully!")

    return redirect("home")

@login_required
def userDashboard(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    my_skills = Skill.objects.filter(user=request.user)

    received_requests = SwapRequest.objects.filter(
        receiver=request.user
    ).order_by('-created_at')

    sent_requests = SwapRequest.objects.filter(
        sender=request.user
    ).order_by('-created_at')

    context = {
        "profile": profile,
        "my_skills": my_skills,
        "received_requests": received_requests,
        "sent_requests": sent_requests,
        "skill_count": my_skills.count(),
        "sent_count": sent_requests.count(),
        "received_count": received_requests.count(),
    }

    return render(request, "userDashboard.html", context)


@login_required
def accept_request(request, request_id):

    swap = SwapRequest.objects.get(id=request_id)

    if swap.receiver != request.user:
        return redirect("userDashboard")

    swap.status = "Accepted"
    swap.save()

    messages.success(request, "Swap request accepted.")

    return redirect("userDashboard")


@login_required
def reject_request(request, request_id):

    swap = SwapRequest.objects.get(id=request_id)

    if swap.receiver != request.user:
        return redirect("userDashboard")

    swap.status = "Rejected"
    swap.save()

    messages.success(request, "Swap request rejected.")

    return redirect("userDashboard")
@login_required
def admin_users(request):

    if not request.user.is_superuser:
        return redirect("home")

    users = User.objects.all().order_by("-date_joined")

    return render(request, "admin/users.html", {
        "users": users
    })


@login_required
def admin_skills(request):

    if not request.user.is_superuser:
        return redirect("home")

    skills = Skill.objects.all().order_by("-id")

    return render(request, "admin/skills.html", {
        "skills": skills
    })


@login_required
def admin_swaps(request):

    if not request.user.is_superuser:
        return redirect("home")

    swaps = SwapRequest.objects.all().order_by("-id")

    return render(request, "admin/swaps.html", {
        "swaps": swaps
    })


@login_required
def admin_premium(request):

    if not request.user.is_superuser:
        return redirect("home")

    profiles = Profile.objects.filter(is_premium=True)

    return render(request, "admin/premium.html", {
        "profiles": profiles
    })


@login_required
def admin_payments(request):

    if not request.user.is_superuser:
        return redirect("home")

    return render(request, "admin/payments.html")


@login_required
def admin_reports(request):

    if not request.user.is_superuser:
        return redirect("home")

    context = {
        "total_users": User.objects.count(),
        "total_skills": Skill.objects.count(),
        "total_premium": Profile.objects.filter(is_premium=True).count(),
    }

    return render(request, "admin/reports.html", context)


@login_required
def admin_settings(request):

    if not request.user.is_superuser:
        return redirect("home")

    return render(request, "admin/settings.html")
    