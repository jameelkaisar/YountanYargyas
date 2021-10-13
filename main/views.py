from django.shortcuts import render, redirect
from .models import StudentClass, StudentSubject, StudentChapter, StudentSection, UploadImage, UploadVideo, UploadAudio, UploadFile, UploadFeed
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import MyRegistrationForm, MyLoginForm, ChangePasswordForm, AddClass, AddSubject, AddChapter, AddSection, AddImage, AddVideo, AddAudio, AddFile, AddFeed, EditClass, EditSubject, EditChapter, EditSection, EditImage, EditVideo, EditAudio, EditFile, EditFeed
from django.core.paginator import Paginator
from django.utils.text import slugify

# Create your views here.

def is_editor(user):
    if user.is_authenticated:
        if user.is_superuser or "teacher" in [g.name for g in user.groups.all()]:
            return True
    return False

def homepage(request):
    return render(
        request=request,
        template_name="main/home.html",
        context={"title": "Home"}
        )

def aboutpage(request):
    return render(
        request=request,
        template_name="main/about.html",
        context={"title": "About"}
        )

def contactpage(request):
    return render(
        request=request,
        template_name="main/contact.html",
        context={"title": "Contact"}
        )

def helppage(request):
    return render(
        request=request,
        template_name="main/help.html",
        context={"title": "Help"}
        )

def register(request):
    if request.user.is_authenticated:
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
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
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect("main:homepage")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        form = MyRegistrationForm
        return render(
            request=request,
            template_name="main/register.html",
            context={"title": "Register", "form": form, "next": request.GET.get('next')})

def login_request(request):
    if request.user.is_authenticated:
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
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
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect("main:homepage")
                else:
                    messages.error(request, "Invalid username or password!")
            else:
                messages.error(request, "Invalid username or password!")

        form = MyLoginForm()
        return render(
            request=request,
            template_name="main/login.html",
            context={"title": "Login", "form": form, "next": request.GET.get('next')})

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
            context={"title": "Change Password", "form": form})
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Logged out successfully!")
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect("main:homepage")

def profile(request):
    if request.user.is_authenticated:
        return render(
            request=request,
            template_name="main/profile.html",
            context={"title": "Profile"}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def upload(request):
    if request.user.is_authenticated:
        return redirect("main:upload_images")
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

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
        upload_image = list(reversed(UploadImage.objects.all()))
        page_upload_image = Paginator(upload_image, 6)
        page_number = request.GET.get('page')
        page_obj = page_upload_image.get_page(page_number)
        return render(
            request=request,
            template_name="main/upload-images.html",
            context={"title": "Images", "editor": is_editor(request.user), "page_obj": page_obj, "form": form, "next": request.get_full_path()}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

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
        upload_video = list(reversed(UploadVideo.objects.all()))
        page_upload_video = Paginator(upload_video, 6)
        page_number = request.GET.get('page')
        page_obj = page_upload_video.get_page(page_number)
        return render(
            request=request,
            template_name="main/upload-videos.html",
            context={"title": "Videos", "editor": is_editor(request.user), "page_obj": page_obj, "form": form, "next": request.get_full_path()}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

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
        upload_audio = list(reversed(UploadAudio.objects.all()))
        page_upload_audio = Paginator(upload_audio, 6)
        page_number = request.GET.get('page')
        page_obj = page_upload_audio.get_page(page_number)
        return render(
            request=request,
            template_name="main/upload-audios.html",
            context={"title": "Audios", "editor": is_editor(request.user), "page_obj": page_obj, "form": form, "next": request.get_full_path()}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

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
        upload_file = list(reversed(UploadFile.objects.all()))
        page_upload_file = Paginator(upload_file, 6)
        page_number = request.GET.get('page')
        page_obj = page_upload_file.get_page(page_number)
        return render(
            request=request,
            template_name="main/upload-files.html",
            context={"title": "Files", "editor": is_editor(request.user), "page_obj": page_obj, "form": form, "next": request.get_full_path()}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def student_feed(request):
    if request.user.is_authenticated:
        return redirect("main:sf_feed")
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def sf_feed(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddFeed(request.POST, request.FILES)
            if form.is_valid():
                form_instance = form.save(commit=False)
                form_instance.feed_user = request.user
                form.save()
                messages.info(request, "Posted Successfully!")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        form = AddFeed()
        upload_feed = UploadFeed.objects.all().order_by('-feed_date')
        page_upload_feed = Paginator(upload_feed, 12)
        page_number = request.GET.get('page')
        page_obj = page_upload_feed.get_page(page_number)
        return render(
            request=request,
            template_name="main/sf-feed.html",
            context={"title": "Feed", "editor": is_editor(request.user), "page_obj": page_obj, "form": form, "next": request.get_full_path()}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def sf_profiles(request):
    if request.user.is_authenticated:
        User = get_user_model()
        users = User.objects.order_by('username')
        page_users = Paginator(users, 12)
        page_number = request.GET.get('page')
        page_obj = page_users.get_page(page_number)
        return render(
            request=request,
            template_name="main/sf-profiles.html",
            context={"title": "Profiles", "editor": is_editor(request.user), "teacher_group": Group.objects.get(name='teacher'), "page_obj": page_obj, "next": request.get_full_path()}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def sf_profile_posts(request, username_slug):
    if request.user.is_authenticated:
        User = get_user_model()
        users = [x.username for x in User.objects.all()]
        if username_slug in users:
            upload_feed = UploadFeed.objects.filter(feed_user=User.objects.get(username=username_slug)).order_by('-feed_date')
            page_upload_feed = Paginator(upload_feed, 12)
            page_number = request.GET.get('page')
            page_obj = page_upload_feed.get_page(page_number)
            return render(
                request=request,
                template_name="main/sf-profile-posts.html",
                context={"title": f"{username_slug}", "editor": is_editor(request.user), "page_obj": page_obj, "total_posts": len(upload_feed), "username_slug": username_slug, "next": request.get_full_path()}
                )
        else:
            messages.error(request, "User not found!")
            return redirect("main:sf_profiles")
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def sf_posts(request):
    if request.user.is_authenticated:
        upload_feed = UploadFeed.objects.filter(feed_user=request.user).order_by('-feed_date')
        page_upload_feed = Paginator(upload_feed, 12)
        page_number = request.GET.get('page')
        page_obj = page_upload_feed.get_page(page_number)
        return render(
            request=request,
            template_name="main/sf-posts.html",
            context={"title": "My Posts", "editor": is_editor(request.user), "page_obj": page_obj, "next": request.get_full_path()}
            )
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect(f"/login?next={request.get_full_path()}")

def student_classes(request):
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
        context={"title": "Classes", "editor": is_editor(request.user), "student_classes": StudentClass.objects.all, "form": form, "next": request.get_full_path()}
        )

def student_class(request, class_slug):
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
            context={"title": class_slug_name, "editor": is_editor(request.user), "student_subjects": matching_subjects, "class_slug": class_slug, "class_slug_name": class_slug_name, "form": form, "next": request.get_full_path()}
            )
    else:
        messages.error(request, f"{class_slug} class is not present!")
        return redirect("main:student_classes")

def student_subject(request, class_slug, subject_slug):
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
                context={"title": subject_slug_name, "editor": is_editor(request.user), "student_chapters": matching_chapters, "class_slug": class_slug, "class_slug_name": class_slug_name, "subject_slug": subject_slug, "subject_slug_name": subject_slug_name, "form": form, "next": request.get_full_path()}
                )
        else:
            messages.error(request, f"{subject_slug} subject is not present!")
            return redirect("main:student_class", class_slug=class_slug)
    else:
        messages.error(request, f"{class_slug} class is not present!")
        return redirect("main:student_classes")

def student_chapter(request, class_slug, subject_slug, chapter_slug):
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
                    context={"title": chapter_slug_name, "editor": is_editor(request.user), "student_sections": matching_sections, "class_slug": class_slug, "class_slug_name": class_slug_name, "subject_slug": subject_slug, "subject_slug_name": subject_slug_name, "chapter_slug": chapter_slug, "chapter_slug_name": chapter_slug_name, "form": form, "next": request.get_full_path()}
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
                        context={"title": section_slug_name, "editor": is_editor(request.user), "student_section": matching_section, "class_slug": class_slug, "class_slug_name": class_slug_name, "subject_slug": subject_slug, "subject_slug_name": subject_slug_name, "chapter_slug": chapter_slug, "chapter_slug_name": chapter_slug_name, "section_slug": section_slug, "section_slug_name": section_slug_name, "next": request.get_full_path()}
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

def delete_data(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get('data_type') == "content" and is_editor(request.user):
                try:
                    instance = StudentSection.objects.get(id=request.POST.get('data_id'))
                    instance.delete()
                    messages.info(request, "Section Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next').rsplit('/', 1)[0])
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "section" and is_editor(request.user):
                try:
                    instance = StudentSection.objects.get(id=request.POST.get('data_id'))
                    instance.delete()
                    messages.info(request, "Section Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "chapter" and is_editor(request.user):
                try:
                    if StudentSection.objects.filter(student_chapter=request.POST.get('data_id')).count():
                        messages.error(request, "Non-empty Chapters can't be Deleted!")
                    else:
                        instance = StudentChapter.objects.get(id=request.POST.get('data_id'))
                        instance.delete()
                        messages.info(request, "Chapter Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "subject" and is_editor(request.user):
                try:
                    if StudentChapter.objects.filter(student_subject=request.POST.get('data_id')).count():
                        messages.error(request, "Non-empty Subjects can't be Deleted!")
                    else:
                        instance = StudentSubject.objects.get(id=request.POST.get('data_id'))
                        instance.delete()
                        messages.info(request, "Subject Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "class" and is_editor(request.user):
                try:
                    if StudentSubject.objects.filter(student_class=request.POST.get('data_id')).count():
                        messages.error(request, "Non-empty Classes can't be Deleted!")
                    else:
                        instance = StudentClass.objects.get(id=request.POST.get('data_id'))
                        instance.delete()
                        messages.info(request, "Class Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "image" and is_editor(request.user):
                try:
                    instance = UploadImage.objects.get(id=request.POST.get('data_id'))
                    instance.delete()
                    messages.info(request, "Image Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "video" and is_editor(request.user):
                try:
                    instance = UploadVideo.objects.get(id=request.POST.get('data_id'))
                    instance.delete()
                    messages.info(request, "Video Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "audio" and is_editor(request.user):
                try:
                    instance = UploadAudio.objects.get(id=request.POST.get('data_id'))
                    instance.delete()
                    messages.info(request, "Audio Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "file" and is_editor(request.user):
                try:
                    instance = UploadFile.objects.get(id=request.POST.get('data_id'))
                    instance.delete()
                    messages.info(request, "File Deleted Successfully!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "post":
                try:
                    instance = UploadFeed.objects.get(id=request.POST.get('data_id'))
                    if instance.feed_user == request.user or is_editor(request.user):
                        instance.delete()
                        messages.info(request, "Post Deleted Successfully!")
                        if request.POST.get('data_next'):
                            return redirect(request.POST.get('data_next'))
                        else:
                            return redirect("main:homepage")
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            else:
                return redirect("main:homepage")
        else:
            return redirect("main:homepage")
    else:
        return redirect("main:homepage")

def edit_data(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get('data_type') == "content" and is_editor(request.user):
                try:
                    instance = StudentSection.objects.get(id=request.POST.get('data_id'))
                    form = EditSection(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "student_section": instance.student_section, "section_summary": instance.section_summary, "section_text": instance.section_text})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Section", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-content" and is_editor(request.user):
                try:
                    instance = StudentSection.objects.get(id=request.POST.get('data_id'))
                    instance.student_section = request.POST.get('student_section')
                    instance.section_summary = request.POST.get('section_summary')
                    instance.section_text = request.POST.get('section_text')
                    # No need to change the video name
                    if instance.section_slug == slugify(instance.student_section):
                        try:
                            instance.save()
                            messages.info(request, "Section Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the section!")
                    else:
                        current_sections = StudentSection.objects.filter(student_chapter=instance.student_chapter)
                        for current_section in current_sections:
                            if current_section.section_slug == slugify(instance.student_section):
                                messages.error(request, f'Section with name \"{instance.student_section}\" already exists.')
                                break
                        else:
                            instance.section_slug = slugify(instance.student_section)
                            try:
                                instance.save()
                                messages.info(request, "Section Edited Successfully!")
                            except:
                                messages.error(request, "Error while saving the section!")
                    if request.POST.get('data_next'):
                        return redirect(f"{request.POST.get('data_next').rsplit('/', 1)[0]}/{instance.section_slug}")
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "section" and is_editor(request.user):
                try:
                    instance = StudentSection.objects.get(id=request.POST.get('data_id'))
                    form = EditSection(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "student_section": instance.student_section, "section_summary": instance.section_summary, "section_text": instance.section_text})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Section", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-section" and is_editor(request.user):
                try:
                    instance = StudentSection.objects.get(id=request.POST.get('data_id'))
                    instance.student_section = request.POST.get('student_section')
                    instance.section_summary = request.POST.get('section_summary')
                    instance.section_text = request.POST.get('section_text')
                    # No need to change the video name
                    if instance.section_slug == slugify(instance.student_section):
                        try:
                            instance.save()
                            messages.info(request, "Section Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the section!")
                    else:
                        current_sections = StudentSection.objects.filter(student_chapter=instance.student_chapter)
                        for current_section in current_sections:
                            if current_section.section_slug == slugify(instance.student_section):
                                messages.error(request, f'Section with name \"{instance.student_section}\" already exists.')
                                break
                        else:
                            instance.section_slug = slugify(instance.student_section)
                            try:
                                instance.save()
                                messages.info(request, "Section Edited Successfully!")
                            except:
                                messages.error(request, "Error while saving the section!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "chapter" and is_editor(request.user):
                try:
                    instance = StudentChapter.objects.get(id=request.POST.get('data_id'))
                    form = EditChapter(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "student_chapter": instance.student_chapter, "chapter_summary": instance.chapter_summary})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Chapter", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-chapter" and is_editor(request.user):
                try:
                    instance = StudentChapter.objects.get(id=request.POST.get('data_id'))
                    instance.student_chapter = request.POST.get('student_chapter')
                    instance.chapter_summary = request.POST.get('chapter_summary')
                    if instance.chapter_slug == slugify(instance.student_chapter):
                        try:
                            instance.save()
                            messages.info(request, "Chapter Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the chapter!")
                    else:
                        current_chapters = StudentChapter.objects.filter(student_subject=instance.student_subject)
                        for current_chapter in current_chapters:
                            if current_chapter.chapter_slug == slugify(instance.student_chapter):
                                messages.error(request, f'Chapter with name \"{instance.student_chapter}\" already exists.')
                                break
                        else:
                            instance.chapter_slug = slugify(instance.student_chapter)
                            try:
                                instance.save()
                                messages.info(request, "Chapter Edited Successfully!")
                            except:
                                messages.error(request, "Error while saving the chapter!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "subject" and is_editor(request.user):
                try:
                    instance = StudentSubject.objects.get(id=request.POST.get('data_id'))
                    form = EditSubject(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "student_subject": instance.student_subject, "subject_summary": instance.subject_summary})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Subject", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-subject" and is_editor(request.user):
                try:
                    instance = StudentSubject.objects.get(id=request.POST.get('data_id'))
                    instance.student_subject = request.POST.get('student_subject')
                    instance.subject_summary = request.POST.get('subject_summary')
                    if instance.subject_slug == slugify(instance.student_subject):
                        try:
                            instance.save()
                            messages.info(request, "Subject Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the subject!")
                    else:
                        current_subjects = StudentSubject.objects.filter(student_class=instance.student_class)
                        for current_subject in current_subjects:
                            if current_subject.subject_slug == slugify(instance.student_subject):
                                messages.error(request, f'Subject with name \"{instance.student_subject}\" already exists.')
                                break
                        else:
                            instance.subject_slug = slugify(instance.student_subject)
                            try:
                                instance.save()
                                messages.info(request, "Subject Edited Successfully!")
                            except:
                                messages.error(request, "Error while saving the subject!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "class" and is_editor(request.user):
                try:
                    instance = StudentClass.objects.get(id=request.POST.get('data_id'))
                    form = EditClass(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "student_class": instance.student_class, "class_summary": instance.class_summary})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Class", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-class" and is_editor(request.user):
                try:
                    instance = StudentClass.objects.get(id=request.POST.get('data_id'))
                    instance.student_class = request.POST.get('student_class')
                    instance.class_summary = request.POST.get('class_summary')
                    if instance.class_slug == slugify(instance.student_class):
                        try:
                            instance.save()
                            messages.info(request, "Class Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the class!")
                    else:
                        current_classes = StudentClass.objects.all()
                        for current_class in current_classes:
                            if current_class.class_slug == slugify(instance.student_class):
                                messages.error(request, f'Class with name \"{instance.student_class}\" already exists.')
                                break
                        else:
                            instance.class_slug = slugify(instance.student_class)
                            try:
                                instance.save()
                                messages.info(request, "Class Edited Successfully!")
                            except:
                                messages.error(request, "Error while saving the class!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "image" and is_editor(request.user):
                try:
                    instance = UploadImage.objects.get(id=request.POST.get('data_id'))
                    form = EditImage(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "image_name": instance.image_name, "image_summary": instance.image_summary})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Image", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-image" and is_editor(request.user):
                try:
                    instance = UploadImage.objects.get(id=request.POST.get('data_id'))
                    instance.image_name = request.POST.get('image_name')
                    instance.image_summary = request.POST.get('image_summary')
                    try:
                        instance.save()
                        messages.info(request, "Image Edited Successfully!")
                    except:
                        messages.error(request, "Error while saving the image!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "video" and is_editor(request.user):
                try:
                    instance = UploadVideo.objects.get(id=request.POST.get('data_id'))
                    form = EditVideo(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "video_name": instance.video_name, "video_summary": instance.video_summary})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Video", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-video" and is_editor(request.user):
                try:
                    instance = UploadVideo.objects.get(id=request.POST.get('data_id'))
                    instance.video_name = request.POST.get('video_name')
                    instance.video_summary = request.POST.get('video_summary')
                    try:
                        instance.save()
                        messages.info(request, "Video Edited Successfully!")
                    except:
                        messages.error(request, "Error while saving the video!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "audio" and is_editor(request.user):
                try:
                    instance = UploadAudio.objects.get(id=request.POST.get('data_id'))
                    form = EditAudio(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "audio_name": instance.audio_name, "audio_summary": instance.audio_summary})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit Audio", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-audio" and is_editor(request.user):
                try:
                    instance = UploadAudio.objects.get(id=request.POST.get('data_id'))
                    instance.audio_name = request.POST.get('audio_name')
                    instance.audio_summary = request.POST.get('audio_summary')
                    try:
                        instance.save()
                        messages.info(request, "Audio Edited Successfully!")
                    except:
                        messages.error(request, "Error while saving the audio!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "file" and is_editor(request.user):
                try:
                    instance = UploadFile.objects.get(id=request.POST.get('data_id'))
                    form = EditFile(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "file_name": instance.file_name, "file_summary": instance.file_summary})
                    return render(
                        request=request,
                        template_name="main/edit-data.html",
                        context={"title": "Edit File", "form": form}
                        )
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-file" and is_editor(request.user):
                try:
                    instance = UploadFile.objects.get(id=request.POST.get('data_id'))
                    instance.file_name = request.POST.get('file_name')
                    instance.file_summary = request.POST.get('file_summary')
                    try:
                        instance.save()
                        messages.info(request, "File Edited Successfully!")
                    except:
                        messages.error(request, "Error while saving the file!")
                    if request.POST.get('data_next'):
                        return redirect(request.POST.get('data_next'))
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "post":
                try:
                    instance = UploadFeed.objects.get(id=request.POST.get('data_id'))
                    if instance.feed_user == request.user:
                        form = EditFeed(initial={"data_id": request.POST.get('data_id'), "data_type": f"edit-{request.POST.get('data_type')}", "data_next": request.POST.get('data_next'), "feed_text": instance.feed_text})
                        return render(
                            request=request,
                            template_name="main/edit-data.html",
                            context={"title": "Edit Post", "form": form}
                            )
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            elif request.POST.get('data_type') == "edit-post":
                try:
                    instance = UploadFeed.objects.get(id=request.POST.get('data_id'))
                    if instance.feed_user == request.user:
                        instance.feed_text = request.POST.get('feed_text')
                        try:
                            instance.save()
                            messages.info(request, "Post Edited Successfully!")
                        except:
                            messages.error(request, "Error while saving the post!")
                        if request.POST.get('data_next'):
                            return redirect(request.POST.get('data_next'))
                        else:
                            return redirect("main:homepage")
                    else:
                        return redirect("main:homepage")
                except:
                    return redirect("main:homepage")
            else:
                return redirect("main:homepage")
        else:
            return redirect("main:homepage")
    else:
        return redirect("main:homepage")
