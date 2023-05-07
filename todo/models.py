# models.py
from django.db import models


class TodoItem(models.Model):
    content = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)


class TodoList(models.Model):
    date = models.DateField()
    todo_items = models.ManyToManyField(TodoItem)
