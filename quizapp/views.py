from django.shortcuts import render, redirect
from . import models as quiz_models
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
import csv

# Create your views here.
@login_required(login_url="quiz:login_user")
def index(request):
    user = quiz_models.AppUser.objects.get(id=request.user.id)
    if user.has_submitted:
        return redirect("quiz:result_page")
    
    question = quiz_models.Question.objects.all().order_by("id")
    # choice = quiz_models.Choices.objects.filter(question=question)
    
    context = {
        "question": question,
        # "choice": choice 
        
    }
    
    return render(request, "index.html", context)

def calculate_score(request):
    question = quiz_models.Question.objects.all().order_by("id")
    user_id = quiz_models.AppUser.objects.get(id=request.user.id)
    if request.method == "POST":
        for quest in question:
            selected_choice_id = request.POST.get(f"choice_{quest.id}")
            
            if selected_choice_id:
                try:
                    selected_choice = quiz_models.Choices.objects.get(id=selected_choice_id)
                
                    if selected_choice.is_correct:
                        # user_id.num_of_correct_choices =  selected_choice.is_correct
                        user_id.score += 2
                        user_id.has_submitted = True
                        user_id.save()
                        
                except quiz_models.Choices.DoesNotExist:
                    pass
                
            with open("./plugin/result.csv", 'a') as file:
                content = [
                    [f"{request.user.first_name} {request.user.last_name}", f"{user_id.score}"]
                ]
                writer = csv.writer(file)
                writer.writerows(content)
                
    return redirect(to="quiz:result_page")

def result_page(request):
    questions = quiz_models.Question.objects.all()
    user_id = quiz_models.AppUser.objects.get(id=request.user.id)
    user_score = user_id.score
    # correct_answers = user_id.num_of_correct_choices
    len_of_questions = len(questions)
    correct_count = quiz_models.Choices.objects.filter(is_correct=True).count()
    
    
    context = {
        "user_score":user_score,
        # "correct_answers":correct_answers,
        "len_of_questions":len_of_questions,
        "correct_count":correct_count,
        
    }
    return render(request, 'result.html', context)
                    
def login_user(request):
    if request.user.is_authenticated:
        return redirect("quiz:index")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pswd")
        
        my_user = authenticate(username=username, password=password)
        
        if my_user is not None:
            login(request, my_user)
            messages.success(request, "Login Successful!!!")
            return redirect(to="quiz:index")
        else:
            messages.error(request, "There was a problem logging you in\nCheck login credentials")
            return redirect(to="quiz:login_user")
        
    return render(request, 'login.html')

def register_user(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sign Up success")
            return redirect("quiz:login_user")
        messages.error(request, "There was a problem!!")
        return redirect("quiz:register_user")
    
    context = {
        "form":form
    }
    return render(request, "register.html", context)
