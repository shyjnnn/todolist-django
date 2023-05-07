# serializers.py
from rest_framework import serializers
from .models import TodoItem, TodoList


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['id', 'content', 'is_done']


# class TodoListSerializer(serializers.ModelSerializer):
#     todo_items = TodoItemSerializer(many=True)

#     class Meta:
#         model = TodoList
#         fields = ['date', 'todo_items']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['todo_items'] = list(reversed(data['todo_items']))
#         return data["todo_items"]
class TodoListSerializer(serializers.ModelSerializer):
    todo_items = TodoItemSerializer(many=True)

    class Meta:
        model = TodoList
        fields = ['date', 'todo_items']

    def to_representation(self, instance, context=None):
        data = super().to_representation(instance)
        if self.context.get('request').method == 'GET':
            if not self.context.get('request').query_params:
                return data
            # return reversed(data['todo_items'])
            return reversed(data['todo_items'])
        # elif self.context.get('request').method == 'POST':

        return data
