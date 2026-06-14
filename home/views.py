from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Skill
from django.http import JsonResponse
def chatbot(request):
    message = request.GET.get("message", "").lower()

    # simple responses (rule-based chatbot)
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
        reply = "Sorry, I didn’t understand. Try asking about skills, login, or register."

    return JsonResponse({"reply": reply})




# HOME PAGE (ONLY DISPLAY DATA)
def home(request):
    skills = Skill.objects.all()
    return render(request, 'home.html', {'skills': skills})


# REGISTER USER
def register_user(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')

    return render(request, 'register.html')


# LOGIN USER
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


# LOGOUT USER
def logout_user(request):
    logout(request)
    return redirect('login')


# ADD SKILL (SAVE DATA)
def add_skill(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        Skill.objects.create(
            user=request.user,
            skill_have=request.POST['skill_have'],
            skill_want=request.POST['skill_want'],
            description=request.POST['description']
        )
        return redirect('home')

    return render(request, 'add_skill.html')


    