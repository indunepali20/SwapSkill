from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill, Profile, SwapRequest
from .models import Skill, Profile, SwapRequest, Message

import json
import requests
from django.db.models import Q
from django.http import JsonResponse
import json

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt



# HOME
def home(request):
    skills = Skill.objects.all()
    return render(request, 'home.html', {'skills': skills})


# CHATBOT

def chatbot(request):

    if request.method == "POST":

        body = json.loads(request.body)

        message = body.get("message", "").lower().strip()

        # Greetings
        if any(word in message for word in [
            "hi","hello","hey","namaste"
        ]):
            answer = (
                "👋 Hello! Welcome to SwapSkill. "
                "How can I help you today?"
            )

        # About SwapSkill
        elif "swapskill" in message or "what is swapskill" in message:
            answer = (
                "SwapSkill is a platform where users exchange skills "
                "instead of paying money."
            )

        # Registration
        elif "register" in message or "signup" in message:
            answer = (
                "Click Register from the navigation bar and create your account."
            )

        # Login
        elif "login" in message:
            answer = (
                "Click Login from the menu and enter your username and password."
            )

        # Add Skill
        elif "add skill" in message or "post skill" in message:
            answer = (
                "Go to Add Skill and enter:\n"
                "• Skill you can teach\n"
                "• Skill you want to learn\n"
                "• Description"
            )

        # Premium
        elif "premium" in message:
            answer = (
                "Premium users receive:\n"
                "⭐ Premium badge\n"
                "⭐ Featured skills\n"
                "⭐ Unlimited swap requests\n"
                "⭐ Higher visibility"
            )

        # Payment
        elif "payment" in message or "khalti" in message:
            answer = (
                "SwapSkill supports Khalti payment for Premium Membership."
            )

        # Dashboard
        elif "dashboard" in message:
            answer = (
                "Open My Dashboard to manage your profile, skills, swap requests, and chats."
            )

        # Chat
        elif "chat" in message or "message" in message:
            answer = (
                "After a swap request is accepted, both users can open the chat and communicate."
            )

        # Request
        elif "swap request" in message or "request skill" in message:
            answer = (
                "Open any skill and click Request Swap. "
                "The owner can Accept or Reject your request."
            )

        # Python
        elif "python" in message:
            answer = (
                "Python is one of the most popular programming languages for web development, AI, automation, and data science."
            )

        # Django
        elif "django" in message:
            answer = (
                "Django is a Python web framework used to build secure and scalable web applications."
            )

        # HTML
        elif "html" in message:
            answer = (
                "HTML is used to create the structure of webpages."
            )

        # CSS
        elif "css" in message:
            answer = (
                "CSS is used to style webpages and make them beautiful."
            )

        # JavaScript
        elif "javascript" in message or "js" in message:
            answer = (
                "JavaScript adds interactivity to websites."
            )

        # Skills
        elif "recommend skill" in message or "popular skill" in message:
            answer = (
                "Popular skills include:\n"
                "• Python\n"
                "• Django\n"
                "• Java\n"
                "• Graphic Design\n"
                "• UI/UX\n"
                "• Digital Marketing\n"
                "• Video Editing"
            )

        # Thanks
        elif "thank" in message:
            answer = (
                "You're welcome! 😊 Happy Skill Swapping!"
            )

        # Bye
        elif "bye" in message:
            answer = (
                "Goodbye! Hope to see you again on SwapSkill 👋"
            )

        # Default
        else:
            answer = (
                "🤖 Sorry, I don't understand that yet.\n"
                "Try asking about:\n"
                "• Register\n"
                "• Premium\n"
                "• Add Skill\n"
                "• Swap Request\n"
                "• Chat\n"
                "• Python\n"
                "• Django"
            )

        return JsonResponse({
            "response": answer
        })



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

from django.db.models import Q

@login_required
def admin_users(request):

    if not request.user.is_superuser:
        return redirect("home")

    search = request.GET.get("search", "")

    users = User.objects.all().order_by("-date_joined")

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    return render(request, "admin/users.html", {
        "users": users,
        "search": search,
        "total_users": users.count(),
    })
@login_required
def delete_user(request, user_id):

    if not request.user.is_superuser:
        return redirect("home")

    user = User.objects.get(id=user_id)

    if user.is_superuser:
        messages.error(request, "You cannot delete the admin account.")
    else:
        user.delete()
        messages.success(request, "User deleted successfully.")

    return redirect("admin_users")



@login_required
def admin_skills(request):

    if not request.user.is_superuser:
        return redirect("home")

    search = request.GET.get("search", "")

    skills = Skill.objects.select_related("user").all().order_by("-created_at")

    if search:
        skills = skills.filter(
            Q(skill_have__icontains=search) |
            Q(skill_want__icontains=search) |
            Q(user__username__icontains=search)
        )

    return render(request, "admin/skills.html", {
        "skills": skills,
        "search": search,
        "total_skills": skills.count(),
    })
@login_required
def delete_skill(request, skill_id):

    if not request.user.is_superuser:
        return redirect("home")

    skill = Skill.objects.get(id=skill_id)
    skill.delete()

    messages.success(request, "Skill deleted successfully.")

    return redirect("admin_skills")
    
@login_required
def admin_swaps(request):

    if not request.user.is_superuser:
        return redirect("home")

    search = request.GET.get("search", "")

    swaps = SwapRequest.objects.select_related(
        "sender",
        "receiver",
        "skill"
    ).all().order_by("-created_at")

    if search:
        swaps = swaps.filter(
            Q(sender__username__icontains=search) |
            Q(receiver__username__icontains=search) |
            Q(skill__skill_have__icontains=search)
        )

    return render(request, "admin/swaps.html", {
        "swaps": swaps,
        "search": search,
        "total_swaps": swaps.count(),
    })


@login_required
def delete_swap(request, swap_id):

    if not request.user.is_superuser:
        return redirect("home")

    swap = SwapRequest.objects.get(id=swap_id)

    swap.delete()

    messages.success(request, "Swap deleted successfully.")

    return redirect("admin_swaps")


@login_required
def admin_premium(request):

    if not request.user.is_superuser:
        return redirect("home")

    search = request.GET.get("search", "")

    profiles = Profile.objects.select_related("user").filter(
        is_premium=True
    )

    if search:
        profiles = profiles.filter(
            user__username__icontains=search
        )

    context = {
        "profiles": profiles,
        "search": search,
        "total": profiles.count()
    }

    return render(
        request,
        "admin/premium.html",
        context
    )


@login_required
def remove_premium(request, profile_id):

    if not request.user.is_superuser:
        return redirect("home")

    profile = Profile.objects.get(id=profile_id)

    profile.is_premium = False
    profile.save()

    messages.success(
        request,
        "Premium removed successfully."
    )

    return redirect("admin_premium")


@login_required
def admin_payments(request):

    if not request.user.is_superuser:
        return redirect("home")

    return render(
        request,
        "admin/payments.html"
    )


@login_required
def admin_reports(request):

    if not request.user.is_superuser:
        return redirect("home")

    context = {
        "users": User.objects.count(),
        "skills": Skill.objects.count(),
        "premium": Profile.objects.filter(
            is_premium=True
        ).count(),
        "swaps": SwapRequest.objects.count(),
        "accepted": SwapRequest.objects.filter(
            status="Accepted"
        ).count(),
        "pending": SwapRequest.objects.filter(
            status="Pending"
        ).count(),
        "rejected": SwapRequest.objects.filter(
            status="Rejected"
        ).count(),
    }

    return render(
        request,
        "admin/reports.html",
        context
    )


@login_required
def admin_settings(request):

    if not request.user.is_superuser:
        return redirect("home")

    return render(
        request,
        "admin/settings.html"
    )


@login_required
def chat(request, swap_id):

    swap = SwapRequest.objects.get(id=swap_id)

    if request.user != swap.sender and request.user != swap.receiver:
        return redirect("home")

    if swap.status != "Accepted":
        messages.error(
            request,
            "Chat is available only after the swap is accepted."
        )
        return redirect("userDashboard")

    if request.method == "POST":

        text = request.POST.get("message")

        if text and text.strip():

            Message.objects.create(
                swap=swap,
                sender=request.user,
                message=text
            )

        return redirect("chat", swap_id=swap.id)

    chat_messages = Message.objects.filter(
        swap=swap
    ).order_by("created_at")

    return render(
        request,
        "chat.html",
        {
            "swap": swap,
            "messages": chat_messages,
        }
    )