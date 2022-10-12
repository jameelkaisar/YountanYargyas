"""YountanYargyas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("about/", views.aboutpage, name="aboutpage"),
    path("contact/", views.contactpage, name="contactpage"),
    path("help/", views.helppage, name="helppage"),
    path("register/", views.register, name="register"),
    path("login/", views.login_request, name="login_request"),
    path("change-password/", views.change_password, name="change_password"),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("admin/", views.admin_section, name="admin_section"),
    # path("upload/", views.upload, name="upload"),
    # path("upload/images", views.upload_images, name="upload_images"),
    # path("upload/videos", views.upload_videos, name="upload_videos"),
    # path("upload/audios", views.upload_audios, name="upload_audios"),
    # path("upload/files", views.upload_files, name="upload_files"),
    path("assembly/", views.assembly, name="assembly"),
    path("community/", views.community_feed, name="community_feed"),
    path("community/feed", views.cf_feed, name="cf_feed"),
    path("community/profiles", views.cf_profiles, name="cf_profiles"),
    path("community/profiles/<slug:username_slug>", views.cf_profile_posts, name="cf_profile_posts"),
    path("community/posts", views.cf_posts, name="cf_posts"),
    # path("messages/", views.messages_section, name="messages_section"),
    # path("messages/<slug:username_slug>", views.messages_chat, name="messages_chat"),
    # path("notifications/", views.notifications, name="notifications"),
    path("classes/", views.student_classes, name="student_classes"),
    path("classes/<slug:class_slug>", views.student_class, name="student_class"),
    path("classes/<slug:class_slug>/<slug:subject_slug>", views.student_subject, name="student_subject"),
    path("classes/<slug:class_slug>/<slug:subject_slug>/<slug:chapter_slug>", views.student_chapter, name="student_chapter"),
    path("classes/<slug:class_slug>/<slug:subject_slug>/<slug:chapter_slug>/<slug:section_slug>", views.student_section, name="student_section"),
    path("student/", views.student_categories, name="student_categories"),
    path("student/<slug:category_slug>", views.student_content, name="student_content"),
    path("delete-data", views.delete_data, name="delete_data"),
    path("edit-data", views.edit_data, name="edit_data"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
