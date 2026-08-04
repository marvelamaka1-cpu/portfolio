from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Skill, Project
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("portfolio:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("portfolio:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("portfolio:register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "portfolio/register.html")


def home(request):
    featured_projects = Project.objects.filter(featured=True)[:3]

    context = {
        "featured_projects": featured_projects,
        "project_count": Project.objects.count(),
        "skill_count": Skill.objects.count(),
    }

    return render(request, "portfolio/home.html", context)


def about(request):
    """About page: bio plus education, experience, and career goal."""
    about_blocks = [
        {'label': 'Education', 'value': 'B.Sc. Computer Science'},
        {'label': 'Experience', 'value': 'Django · Python · HTML · CSS · JavaScript'},
        {'label': 'Career Goal', 'value': "To build innovative web applications that improve people's lives."},
    ]
    return render(request, 'portfolio/about.html', {'about_blocks': about_blocks})


def skills(request):
    """Skills page, now pulling real rows from the Skill model."""
    skill_list = Skill.objects.all()
    return render(request, 'portfolio/skills.html', {'skill_list': skill_list})



def projects(request):
    project_list = Project.objects.all().order_by("-created_at")
    return render(
        request,
        "portfolio/projects.html",
        {"project_list": project_list},
    )


def contact(request):
    sent = False

    if request.method == "POST":
        full_name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if full_name and email and message:

            Contact.objects.create(
                full_name=full_name,
                subject="Portfolio Contact Form",
                email=email,
                message=message,
            )

            send_mail(
                subject=f"New Portfolio Message from {full_name}",
                message=f"""
Name: {full_name}

Email: {email}

Message:
{message}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            sent = True

    return render(request, "portfolio/contact.html", {"sent": sent})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "portfolio/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

def project_detail(request, pk):

    project = get_object_or_404(Project, pk=pk)

    return render(
        request,
        "portfolio/project_detail.html",
        {"project": project},
    )

