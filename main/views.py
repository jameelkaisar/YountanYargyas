from django.shortcuts import render, redirect
from .models import Book, StudentClass, StudentSubject, StudentChapter, StudentSection
from django.http import HttpResponse
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

def student_classes(request):
    # return HttpResponse("Hello <strong>World</strong>!")
    return render(
        request=request,
        template_name="main/classes.html",
        context={"student_classes": StudentClass.objects.all}
        )

def student_class(request, class_slug):
    class_slugs = [c.class_slug for c in StudentClass.objects.all()]
    if class_slug in class_slugs:
        matching_subjects = StudentSubject.objects.filter(student_class__class_slug=class_slug)
        return render(
            request=request,
            template_name="main/subjects.html",
            context={"student_subjects": matching_subjects, "class_slug": class_slug}
            )
    else:
        return HttpResponse(f"{class_slug} class is not present!")

def student_subject(request, class_slug, subject_slug):
    class_slugs = [c.class_slug for c in StudentClass.objects.all()]
    if class_slug in class_slugs:
        matching_subjects = StudentSubject.objects.filter(student_class__class_slug=class_slug)
        subject_slugs = [s.subject_slug for s in matching_subjects]
        if subject_slug in subject_slugs:
            matching_chapters = StudentChapter.objects.filter(student_subject__subject_slug=subject_slug, student_subject__student_class__class_slug=class_slug)
            return render(
                request=request,
                template_name="main/chapters.html",
                context={"student_chapters": matching_chapters, "class_slug": class_slug, "subject_slug": subject_slug}
                )
        else:
            return HttpResponse(f"{subject_slug} subject is not present!")
    else:
        return HttpResponse(f"{class_slug} class is not present!")

def student_chapter(request, class_slug, subject_slug, chapter_slug):
    class_slugs = [c.class_slug for c in StudentClass.objects.all()]
    if class_slug in class_slugs:
        matching_subjects = StudentSubject.objects.filter(student_class__class_slug=class_slug)
        subject_slugs = [s.subject_slug for s in matching_subjects]
        if subject_slug in subject_slugs:
            matching_chapters = StudentChapter.objects.filter(student_subject__subject_slug=subject_slug, student_subject__student_class__class_slug=class_slug)
            chapter_slugs = [c.chapter_slug for c in matching_chapters]
            if chapter_slug in chapter_slugs:
                matching_sections = StudentSection.objects.filter(student_chapter__chapter_slug=chapter_slug, student_chapter__student_subject__subject_slug=subject_slug, student_chapter__student_subject__student_class__class_slug=class_slug)
                return render(
                    request=request,
                    template_name="main/sections.html",
                    context={"student_sections": matching_sections, "class_slug": class_slug, "subject_slug": subject_slug, "chapter_slug": chapter_slug}
                    )
            else:
                return HttpResponse(f"{chapter_slug} chapter is not present!")
        else:
            return HttpResponse(f"{subject_slug} subject is not present!")
    else:
        return HttpResponse(f"{class_slug} class is not present!")

def student_section(request, class_slug, subject_slug, chapter_slug, section_slug):
    class_slugs = [c.class_slug for c in StudentClass.objects.all()]
    if class_slug in class_slugs:
        matching_subjects = StudentSubject.objects.filter(student_class__class_slug=class_slug)
        subject_slugs = [s.subject_slug for s in matching_subjects]
        if subject_slug in subject_slugs:
            matching_chapters = StudentChapter.objects.filter(student_subject__subject_slug=subject_slug, student_subject__student_class__class_slug=class_slug)
            chapter_slugs = [c.chapter_slug for c in matching_chapters]
            if chapter_slug in chapter_slugs:
                matching_sections = StudentSection.objects.filter(student_chapter__chapter_slug=chapter_slug, student_chapter__student_subject__subject_slug=subject_slug, student_chapter__student_subject__student_class__class_slug=class_slug)
                section_slugs = [s.section_slug for s in matching_sections]
                if section_slug in section_slugs:
                    matching_section = matching_sections.filter(section_slug=section_slug)[0]
                    return render(
                        request=request,
                        template_name="main/content.html",
                        context={"student_section": matching_section, "class_slug": class_slug, "subject_slug": subject_slug, "chapter_slug": chapter_slug, "section_slug": section_slug}
                        )
                else:
                    return HttpResponse(f"{section_slug} section is not present!")
            else:
                return HttpResponse(f"{chapter_slug} chapter is not present!")
        else:
            return HttpResponse(f"{subject_slug} subject is not present!")
    else:
        return HttpResponse(f"{class_slug} class is not present!")
