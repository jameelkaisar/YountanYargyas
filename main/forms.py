from django import forms
from .models import StudentClass, StudentSubject, StudentChapter, StudentSection
from tinymce.widgets import TinyMCE

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
