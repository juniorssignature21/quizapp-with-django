from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AppUser, Discipline, Question, Choices
from django.forms import inlineformset_factory


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control rounded", "placeholder": "First name"}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control rounded", "placeholder": "Last name"}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control rounded", "placeholder": "Username"}), required=True)
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), widget=forms.Select(attrs={"class":"form-control rounded"}))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control rounded", "placeholder": "Password"}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control rounded", "placeholder": "Confirm Password"}), required=True)
    
    class Meta:
        model = AppUser
        fields = ["first_name","last_name","username", "discipline","password1","password2"]
        
class QuestionForm(forms.ModelForm):
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), widget=forms.Select(attrs={"class":"form-control rounded"}), required=True)
    instructor = forms.ModelChoiceField(queryset=AppUser.objects.all(), widget=forms.HiddenInput(attrs={"value":"{{request.user}}"}))
    question_text = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control rounded", "placeholder": "Question", "rows":3}), required=True)
    class Meta:
        model = Question
        fields = [ "instructor",'discipline', 'question_text']
        
ChoiceFormSet = inlineformset_factory(
    parent_model=Question,
    model=Choices,
    fields = ('choice_text', 'option', 'is_correct'),
    extra=4,  # This determines how many empty forms show up
    can_delete=True,  # Allow deletion if you want to replace existing choices
    max_num=4,  # Maximum total choices allowed
    widgets={
        'choice_text': forms.TextInput(attrs={'class': 'form-control'}),
        'option': forms.Select(attrs={'class': 'form-control'}),
        'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
)