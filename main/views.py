from django.shortcuts import render, redirect
from .models import Book
# from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


# Create your views here.

def homepage(request):
    # return HttpResponse("Hello <strong>World</strong>!")
    return render(
        request=request,
        template_name="main/home.html",
        context={"books": Book.objects.all}
        )

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}!")
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = UserCreationForm
    return render(
        request=request,
        template_name="main/register.html",
        context={"form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password  = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}!")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password!")
        else:
            messages.error(request, "Invalid username or password!")

    form = AuthenticationForm()
    return render(
        request=request,
        template_name="main/login.html",
        context={"form": form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")
