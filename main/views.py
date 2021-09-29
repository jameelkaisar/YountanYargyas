from django.shortcuts import render, redirect
from .models import StudentClass, StudentSubject, StudentChapter, StudentSection, UploadImage, UploadVideo, UploadAudio, UploadFile
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from .forms import MyRegistrationForm, MyLoginForm, ChangePasswordForm, AddClass, AddSubject, AddChapter, AddSection, AddImage, AddVideo, AddAudio, AddFile

# Create your views here.

def homepage(request):
    return render(
        request=request,
        template_name="main/home.html"
        )

def aboutpage(request):
    return render(
        request=request,
        template_name="main/about.html"
        )

def contactpage(request):
    return render(
        request=request,
        template_name="main/contact.html"
        )

def helppage(request):
    return render(
        request=request,
        template_name="main/help.html"
        )

def register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect("main:homepage")
    else:
        if request.method == "POST":
            form = MyRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get("username")
                messages.info(request, f"New Account Created: {username}")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}!")
                return redirect("main:homepage")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        form = MyRegistrationForm
        return render(
            request=request,
            template_name="main/register.html",
            context={"form": form})

def login_request(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect("main:homepage")
    else:
        if request.method == "POST":
            form = MyLoginForm(request, request.POST)
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

        form = MyLoginForm()
        return render(
            request=request,
            template_name="main/login.html",
            context={"form": form})

def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.info(request, "Your password was changed successfully!")
                return redirect("main:profile")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        form = ChangePasswordForm(request.user)
        return render(
            request=request,
            template_name="main/change_password.html",
            context={"form": form})
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect("main:login_request")

def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def profile(request):
    if request.user.is_authenticated:
        return render(
            request=request,
            template_name="main/profile.html"
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect("main:login_request")

def upload(request):
    if request.user.is_authenticated:
        return redirect("main:upload_images")
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect("main:login_request")

def upload_images(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddImage(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.info(request, "Image Uploaded Successfully!")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        form = AddImage()
        return render(
            request=request,
            template_name="main/upload-images.html",
            context={"upload_image": UploadImage.objects.all, "form": form}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect("main:login_request")

def upload_videos(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddVideo(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.info(request, "Video Uploaded Successfully!")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        form = AddVideo()
        return render(
            request=request,
            template_name="main/upload-videos.html",
            context={"upload_video": UploadVideo.objects.all, "form": form}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect("main:login_request")

def upload_audios(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddAudio(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.info(request, "Audio Uploaded Successfully!")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        form = AddAudio()
        return render(
            request=request,
            template_name="main/upload-audios.html",
            context={"upload_audio": UploadAudio.objects.all, "form": form}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect("main:login_request")

def upload_files(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddFile(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.info(request, "File Uploaded Successfully!")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        form = AddFile()
        return render(
            request=request,
            template_name="main/upload-files.html",
            context={"upload_file": UploadFile.objects.all, "form": form}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect("main:login_request")

def student_classes(request):
    # Add Edit/Delete Class Form?
    if request.method == "POST":
        form = AddClass(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Class Added Successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    form = AddClass()
    return render(
        request=request,
        template_name="main/classes.html",
        context={"student_classes": StudentClass.objects.all, "form": form}
        )

def student_class(request, class_slug):
    # Add Edit/Delete Subject Form?
    class_slugs = [c.class_slug for c in StudentClass.objects.all()]
    if class_slug in class_slugs:
        class_slug_name = StudentClass.objects.filter(class_slug=class_slug)[0].student_class
        matching_subjects = StudentSubject.objects.filter(student_class__class_slug=class_slug)
        
        if request.method == "POST":
            form = AddSubject(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, "Subject Added Successfully!")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        form = AddSubject(initial={"student_class": StudentClass.objects.filter(class_slug=class_slug)[0]})
        return render(
            request=request,
            template_name="main/subjects.html",
            context={"student_subjects": matching_subjects, "class_slug": class_slug, "class_slug_name": class_slug_name, "form": form}
            )
    else:
        messages.error(request, f"{class_slug} class is not present!")
        return redirect("main:student_classes")

def student_subject(request, class_slug, subject_slug):
    # Add Edit/Delete Chapter Form?
    class_slugs = [c.class_slug for c in StudentClass.objects.all()]
    if class_slug in class_slugs:
        class_slug_name = StudentClass.objects.filter(class_slug=class_slug)[0].student_class
        matching_subjects = StudentSubject.objects.filter(student_class__class_slug=class_slug)
        subject_slugs = [s.subject_slug for s in matching_subjects]
        if subject_slug in subject_slugs:
            subject_slug_name = StudentSubject.objects.filter(subject_slug=subject_slug, student_class__class_slug=class_slug)[0].student_subject
            matching_chapters = StudentChapter.objects.filter(student_subject__subject_slug=subject_slug, student_subject__student_class__class_slug=class_slug)

            if request.method == "POST":
                form = AddChapter(request.POST)
                if form.is_valid():
                    form.save()
                    messages.info(request, "Chapter Added Successfully!")
                else:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, error)

            form = AddChapter(initial={"student_subject": StudentSubject.objects.filter(subject_slug=subject_slug, student_class__class_slug=class_slug)[0]})
            return render(
                request=request,
                template_name="main/chapters.html",
                context={"student_chapters": matching_chapters, "class_slug": class_slug, "class_slug_name": class_slug_name, "subject_slug": subject_slug, "subject_slug_name": subject_slug_name, "form": form}
                )
        else:
            messages.error(request, f"{subject_slug} subject is not present!")
            return redirect("main:student_class", class_slug=class_slug)
    else:
        messages.error(request, f"{class_slug} class is not present!")
        return redirect("main:student_classes")

def student_chapter(request, class_slug, subject_slug, chapter_slug):
    # Add Edit/Delete Section Form?
    class_slugs = [c.class_slug for c in StudentClass.objects.all()]
    if class_slug in class_slugs:
        class_slug_name = StudentClass.objects.filter(class_slug=class_slug)[0].student_class
        matching_subjects = StudentSubject.objects.filter(student_class__class_slug=class_slug)
        subject_slugs = [s.subject_slug for s in matching_subjects]
        if subject_slug in subject_slugs:
            subject_slug_name = StudentSubject.objects.filter(subject_slug=subject_slug, student_class__class_slug=class_slug)[0].student_subject
            matching_chapters = StudentChapter.objects.filter(student_subject__subject_slug=subject_slug, student_subject__student_class__class_slug=class_slug)
            chapter_slugs = [c.chapter_slug for c in matching_chapters]
            if chapter_slug in chapter_slugs:
                chapter_slug_name = StudentChapter.objects.filter(chapter_slug=chapter_slug, student_subject__subject_slug=subject_slug, student_subject__student_class__class_slug=class_slug)[0].student_chapter
                matching_sections = StudentSection.objects.filter(student_chapter__chapter_slug=chapter_slug, student_chapter__student_subject__subject_slug=subject_slug, student_chapter__student_subject__student_class__class_slug=class_slug)

                if request.method == "POST":
                    form = AddSection(request.POST, request.FILES)
                    if form.is_valid():
                        form_instance = form.save(commit=False)
                        # Change on completely hiding Foreign Key field
                        # Override Save Method?
                        form_instance.section_video_base = f"classes/{class_slug}/{subject_slug}/{chapter_slug}/"
                        form.save()
                        messages.info(request, "Section Added Successfully!")
                    else:
                        for field, errors in form.errors.items():
                            for error in errors:
                                messages.error(request, error)

                form = AddSection(initial={"student_chapter": StudentChapter.objects.filter(chapter_slug=chapter_slug, student_subject__subject_slug=subject_slug, student_subject__student_class__class_slug=class_slug)[0]})
                return render(
                    request=request,
                    template_name="main/sections.html",
                    context={"student_sections": matching_sections, "class_slug": class_slug, "class_slug_name": class_slug_name, "subject_slug": subject_slug, "subject_slug_name": subject_slug_name, "chapter_slug": chapter_slug, "chapter_slug_name": chapter_slug_name, "form": form}
                    )
            else:
                messages.error(request, f"{chapter_slug} chapter is not present!")
                return redirect("main:student_subject", class_slug=class_slug, subject_slug=subject_slug)
        else:
            messages.error(request, f"{subject_slug} subject is not present!")
            return redirect("main:student_class", class_slug=class_slug)
    else:
        messages.error(request, f"{class_slug} class is not present!")
        return redirect("main:student_classes")

def student_section(request, class_slug, subject_slug, chapter_slug, section_slug):
    # Add Edit/Delete Section Form?
    class_slugs = [c.class_slug for c in StudentClass.objects.all()]
    if class_slug in class_slugs:
        class_slug_name = StudentClass.objects.filter(class_slug=class_slug)[0].student_class
        matching_subjects = StudentSubject.objects.filter(student_class__class_slug=class_slug)
        subject_slugs = [s.subject_slug for s in matching_subjects]
        if subject_slug in subject_slugs:
            subject_slug_name = StudentSubject.objects.filter(subject_slug=subject_slug, student_class__class_slug=class_slug)[0].student_subject
            matching_chapters = StudentChapter.objects.filter(student_subject__subject_slug=subject_slug, student_subject__student_class__class_slug=class_slug)
            chapter_slugs = [c.chapter_slug for c in matching_chapters]
            if chapter_slug in chapter_slugs:
                chapter_slug_name = StudentChapter.objects.filter(chapter_slug=chapter_slug, student_subject__subject_slug=subject_slug, student_subject__student_class__class_slug=class_slug)[0].student_chapter
                matching_sections = StudentSection.objects.filter(student_chapter__chapter_slug=chapter_slug, student_chapter__student_subject__subject_slug=subject_slug, student_chapter__student_subject__student_class__class_slug=class_slug)
                section_slugs = [s.section_slug for s in matching_sections]
                if section_slug in section_slugs:
                    section_slug_name = StudentSection.objects.filter(section_slug=section_slug, student_chapter__chapter_slug=chapter_slug, student_chapter__student_subject__subject_slug=subject_slug, student_chapter__student_subject__student_class__class_slug=class_slug)[0].student_section
                    matching_section = matching_sections.filter(section_slug=section_slug)[0]
                    return render(
                        request=request,
                        template_name="main/content.html",
                        context={"student_section": matching_section, "class_slug": class_slug, "class_slug_name": class_slug_name, "subject_slug": subject_slug, "subject_slug_name": subject_slug_name, "chapter_slug": chapter_slug, "chapter_slug_name": chapter_slug_name, "section_slug": section_slug, "section_slug_name": section_slug_name}
                        )
                else:
                    messages.error(request, f"{section_slug} section is not present!")
                    return redirect("main:student_chapter", class_slug=class_slug, subject_slug=subject_slug, chapter_slug=chapter_slug)
            else:
                messages.error(request, f"{chapter_slug} chapter is not present!")
                return redirect("main:student_subject", class_slug=class_slug, subject_slug=subject_slug)
        else:
            messages.error(request, f"{subject_slug} subject is not present!")
            return redirect("main:student_class", class_slug=class_slug)
    else:
        messages.error(request, f"{class_slug} class is not present!")
        return redirect("main:student_classes")
