from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path('', views.index, name="index"),
    path('quiz_page/', views.home, name="quiz_page"),
    path('calculate_score/', views.calculate_score, name="calculate_score"),
    path('result_page/', views.result_page, name="result_page"),
    path('login_user/', views.login_user, name="login_user"),
    path('register_user/', views.register_user, name="register_user"),
    path('add_question/', views.add_question, name="add_question"),
    path('question_list/<int:pk>/', views.question_list, name="question_list"),
    path('question/edit/<int:question_id>/', views.edit_question, name='edit_question'),    
]
