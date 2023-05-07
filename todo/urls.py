from django.urls import path
from .views import TodoListView, TodoDateListView, TodoItemView

urlpatterns = [
    path('todo/', TodoListView.as_view(), name='todo'),
    path('dotdates/', TodoDateListView.as_view(), name='dotdates'),
    path('todo/<int:pk>/', TodoItemView.as_view()),
]
