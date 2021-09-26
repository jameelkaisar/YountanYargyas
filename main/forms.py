from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import StudentClass, StudentSubject, StudentChapter, StudentSection
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
        widgets = {"section_summary": forms.Textarea(attrs={"class": "materialize-textarea"}), "section_video": forms.FileInput(attrs={"style": "display: none;"}), "section_text": TinyMCE(), "student_chapter": forms.HiddenInput()}
