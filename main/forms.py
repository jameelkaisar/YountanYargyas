from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import StudentClass, StudentSubject, StudentChapter, StudentSection, UploadImage, UploadVideo, UploadAudio, UploadFile, UploadFeed
from tinymce.widgets import TinyMCE

class MyRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(MyRegistrationForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={"autocapitalize": "none", "autocomplete": "username", "maxlength": "150", "autofocus": "autofocus"}), label="Username")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), label="Confirm Password")

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "autofocus": "autofocus"}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}), label="Confirm New Password")

class MyLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={"autocapitalize": "none", "autocomplete": "username", "maxlength": "150", "autofocus": "autofocus"}), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}), label="Password")

class AddClass(forms.ModelForm):
    class Meta:
        model = StudentClass
        fields = ["student_class", "class_summary"]
        labels = {"student_class": "Class Name", "class_summary": "Class Summary"}
        widgets = {"class_summary": forms.Textarea(attrs={"class": "materialize-textarea"})}

class AddSubject(forms.ModelForm):
    class Meta:
        model = StudentSubject
        fields = ["student_subject", "subject_summary", "student_class"]
        labels = {"student_subject": "Subject Name", "subject_summary": "Subject Summary", "student_class": "Student Class (FK)"}
        widgets = {"subject_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "student_class": forms.HiddenInput()}

class AddChapter(forms.ModelForm):
    class Meta:
        model = StudentChapter
        fields = ["student_chapter", "chapter_summary", "student_subject"]
        labels = {"student_chapter": "Chapter Name", "chapter_summary": "Chapter Summary", "student_subject": "Student Subject (FK)"}
        widgets = {"chapter_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "student_subject": forms.HiddenInput()}

class AddSection(forms.ModelForm):
    class Meta:
        model = StudentSection
        fields = ["student_section", "section_summary", "section_video", "section_text", "student_chapter"]
        labels = {"student_section": "Section Name", "section_summary": "Section Summary", "section_video": "", "section_text": "Section Text", "student_chapter": "Student Chapter (FK)"}
        widgets = {"section_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "section_video": forms.FileInput(attrs={"style": "display: none;", "accept": "video/*"}), "section_text": TinyMCE(), "student_chapter": forms.HiddenInput()}

class AddImage(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ["image_name", "image_summary", "image_file"]
        labels = {"image_name": "Image Name", "image_summary": "Image Summary", "image_file": ""}
        widgets = {"image_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "image_file": forms.FileInput(attrs={"style": "display: none;", "accept": "image/*"})}

class AddVideo(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = ["video_name", "video_summary", "video_file"]
        labels = {"video_name": "Video Name", "video_summary": "Video Summary", "video_file": ""}
        widgets = {"video_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "video_file": forms.FileInput(attrs={"style": "display: none;", "accept": "video/*"})}

class AddAudio(forms.ModelForm):
    class Meta:
        model = UploadAudio
        fields = ["audio_name", "audio_summary", "audio_file"]
        labels = {"audio_name": "Audio Name", "audio_summary": "Audio Summary", "audio_file": ""}
        widgets = {"audio_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "audio_file": forms.FileInput(attrs={"style": "display: none;", "accept": "audio/*"})}

class AddFile(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ["file_name", "file_summary", "file_file"]
        labels = {"file_name": "File Name", "file_summary": "File Summary", "file_file": ""}
        widgets = {"file_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "file_file": forms.FileInput(attrs={"style": "display: none;"})}

class AddFeed(forms.ModelForm):
    class Meta:
        model = UploadFeed
        fields = ["feed_text", "feed_file"]
        labels = {"feed_text": "Text", "feed_file": ""}
        widgets = {"feed_text": forms.Textarea(attrs={"class": "materialize-textarea"}), "feed_file": forms.FileInput(attrs={"style": "display: none;"})}

class EditClass(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    student_class = forms.CharField(label="Class Name", max_length=100)
    class_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Class Summary")

class EditSubject(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    student_subject = forms.CharField(label="Subject Name", max_length=100)
    subject_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Subject Summary")

class EditChapter(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    student_chapter = forms.CharField(label="Chapter Name", max_length=100)
    chapter_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Chapter Summary")

class EditSection(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    student_section = forms.CharField(label="Section Name", max_length=100)
    section_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Section Summary")
    section_text = forms.CharField(widget=TinyMCE(), label="Section Text")

class EditImage(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    image_name = forms.CharField(label="Image Name", max_length=100)
    image_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Image Summary")

class EditVideo(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    video_name = forms.CharField(label="Video Name", max_length=100)
    video_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Video Summary")

class EditAudio(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    audio_name = forms.CharField(label="Audio Name", max_length=100)
    audio_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Audio Summary")

class EditFile(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    file_name = forms.CharField(label="File Name", max_length=100)
    file_summary = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="File Summary")

class EditFeed(forms.Form):
    data_id = forms.CharField(widget=forms.HiddenInput())
    data_type = forms.CharField(widget=forms.HiddenInput())
    data_next = forms.CharField(widget=forms.HiddenInput())
    feed_text = forms.CharField(widget=forms.Textarea(attrs={"class": "materialize-textarea"}), label="Text", max_length=5000)
