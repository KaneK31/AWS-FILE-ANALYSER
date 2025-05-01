from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User


def home_view(request):
    return render(request, "filemanager/home.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return HttpResponse("❌ Username already taken.")

        User.objects.create_user(username=username, password=password)
        return HttpResponse("✅ Signup successful!")

    return render(request, "filemanager/signup.html")
