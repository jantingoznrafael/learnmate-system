from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.home, name='home'),
    path('strands/', views.strands, name='strands'),
    path('strands/<str:strand>/', views.strand_detail, name='strand_detail'),
    path('ask/', views.ask_question, name='ask'),
    path('my-questions/', views.my_questions, name='my_questions'),
    path('question/<int:pk>/', views.question_detail, name='detail'),
    path('question/<int:pk>/edit/', views.edit_question, name='edit'),
    path('question/<int:pk>/delete/', views.delete_question, name='delete'),
    path('question/<int:pk>/report/', views.reported_question, name='report'),

]

