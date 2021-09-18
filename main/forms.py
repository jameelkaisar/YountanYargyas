from django import forms
from .models import StudentClass, StudentSubject, StudentChapter, StudentSection
 
class AddClass(forms.ModelForm):
    class Meta:
        model = StudentClass
        fields = ["student_class", "class_summary", "class_slug"]
        labels = {"student_class": "Student Class", "class_summary": "Class Summary", "class_slug": "Class Slug"}

class AddSubject(forms.ModelForm):
    class Meta:
        model = StudentSubject
        fields = ["student_subject", "subject_summary", "subject_slug", "student_class"]
        labels = {"student_subject": "Student Subject", "subject_summary": "Subject Summary", "subject_slug": "Subject Slug", "student_class": "Student Class (FK)"}
        widgets = {"student_class": forms.HiddenInput()}

class AddChapter(forms.ModelForm):
    class Meta:
        model = StudentChapter
        fields = ["student_chapter", "chapter_summary", "chapter_slug", "student_subject"]
        labels = {"student_chapter": "Student Chapter", "chapter_summary": "Chapter Summary", "chapter_slug": "Chapter Slug", "student_subject": "Student Subject (FK)"}
        widgets = {"student_subject": forms.HiddenInput()}

class AddSection(forms.ModelForm):
    class Meta:
        model = StudentSection
        fields = ["student_section", "section_summary", "section_slug", "section_text", "student_chapter"]
        labels = {"student_section": "Student Section", "section_summary": "Section Summary", "section_slug": "Section Slug", "section_text": "Section Text", "student_chapter": "Student Chapter (FK)"}
        widgets = {"student_chapter": forms.HiddenInput()}
