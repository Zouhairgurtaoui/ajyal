from django.urls import path,include
from . import views

urlpatterns = [
    path('student/', include(([
    path('',views.StudentQuizListView.as_view(),name='quiz_list'),
    path('take-quiz/<int:pk>',views.take_quiz,name='take_quiz'),
    path('taken/', views.TakenQuizListView.as_view(), name='taken_quiz_list'),
   ],'quiz'),namespace='student')),

    path('teacher/', include(([
    path('',views.QuizListView.as_view(),name='quiz_change_list'),
    path('add/', views.QuizCreateView.as_view(), name='quiz_add'),
    path('<int:pk>/', views.QuizUpdateView.as_view(), name='quiz_change'),
    path('<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),
    path('<int:pk>/results/', views.QuizResultsView.as_view(), name='quiz_results'),
    path('<int:pk>/question/add/', views.question_add, name='question_add'),
    path('<int:quiz_pk>/question/<int:question_pk>/', views.question_change, name='question_change'),
    path('<int:quiz_pk>/question/<int:question_pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
   ],'quiz'),namespace='teacher')),
]

htmx_urlpatterns =[
    path('search-quiz/',views.search_quiz,name='search-quiz'),
]

urlpatterns += htmx_urlpatterns