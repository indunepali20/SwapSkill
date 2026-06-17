from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Skill, Profile
from django.db.models import Count




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


# PREMIUM
@login_required
def premium(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.is_premium = True
        profile.save()
        return redirect('home')

    return render(request, 'premium.html')


# REGISTER
def register_user(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')

    return render(request, 'register.html')


# LOGIN
def login_user(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# LOGOUT
def logout_user(request):
    logout(request)
    return redirect('login')


# ADD SKILL
@login_required
def add_skill(request):
    if request.method == "POST":
        Skill.objects.create(
            user=request.user,
            skill_have=request.POST['skill_have'],
            skill_want=request.POST['skill_want'],
            description=request.POST['description']
        )
        return redirect('home')

    return render(request, 'add_skill.html')




#dashboard

@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('home')

    total_users = User.objects.count()
    total_skills = Skill.objects.count()
    total_premium = Profile.objects.filter(is_premium=True).count()

    # SAFE queries (no crash)
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    recent_skills = Skill.objects.all().order_by('-id')[:5]

    return render(request, 'admin/dashboard.html', {
        'total_users': total_users,
        'total_skills': total_skills,
        'total_premium': total_premium,
        'recent_users': recent_users,
        'recent_skills': recent_skills,
    })