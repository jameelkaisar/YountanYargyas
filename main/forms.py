from django import forms
from .models import StudentClass, StudentSubject, StudentChapter, StudentSection
 
class AddClass(forms.ModelForm):
    class Meta:
        model = StudentClass
        fields = ["student_class", "class_summary"]
        labels = {"student_class": "Student Class", "class_summary": "Class Summary"}
        widgets = {"class_summary": forms.Textarea}

class AddSubject(forms.ModelForm):
    class Meta:
        model = StudentSubject
        fields = ["student_subject", "subject_summary", "student_class"]
        labels = {"student_subject": "Student Subject", "subject_summary": "Subject Summary", "student_class": "Student Class (FK)"}
        widgets = {"subject_summary": forms.Textarea, "student_class": forms.HiddenInput}

class AddChapter(forms.ModelForm):
    class Meta:
        model = StudentChapter
        fields = ["student_chapter", "chapter_summary", "student_subject"]
        labels = {"student_chapter": "Student Chapter", "chapter_summary": "Chapter Summary", "student_subject": "Student Subject (FK)"}
        widgets = {"chapter_summary": forms.Textarea, "student_subject": forms.HiddenInput}

class AddSection(forms.ModelForm):
    class Meta:
        model = StudentSection
        fields = ["student_section", "section_summary", "section_text", "student_chapter"]
        labels = {"student_section": "Student Section", "section_summary": "Section Summary", "section_text": "Section Text", "student_chapter": "Student Chapter (FK)"}
        widgets = {"section_summary": forms.Textarea, "student_chapter": forms.HiddenInput}
