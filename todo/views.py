from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import TodoItem, TodoList
from .serializers import TodoItemSerializer, TodoListSerializer

class TodoListView(generics.ListCreateAPIView):
    serializer_class = TodoListSerializer

    def create(self, request, *args, **kwargs):
        # 요청 데이터에서 date와 todo_items 추출
        date_str = request.data.get('date')
        todo_items_data = request.data.get('todo_items')

        # date_str을 파싱하여 datetime.date 객체로 변환
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'date': '올바른 날짜 형식이 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 date를 가지는 TodoList가 이미 존재하는지 확인
        todo_list = TodoList.objects.filter(date=date).first()

        # 존재하지 않는다면 새로 생성
        if not todo_list:
            todo_list = TodoList.objects.create(date=date)

        # todo_items를 TodoItem 객체로 변환하여 todo_list에 추가
        todo_items = []
        for item_data in todo_items_data:
            serializer = TodoItemSerializer(data=item_data,context={'request': request})
            serializer.is_valid(raise_exception=True)
            item = serializer.save()
            todo_items.append(item)
            
            
        todo_list.todo_items.add(*todo_items)

        # 생성된 TodoList를 반환
        serializer = self.get_serializer(todo_list)
        # return Response(serializer.data["todo_items"], status=status.HTTP_201_CREATED)
        return Response(reversed(serializer.data["todo_items"]), status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = TodoList.objects.all()
        date_str = self.request.query_params.get('date')
        if date_str:
            # 요청 파라미터에서 date가 주어졌다면 해당 date를 가지는 TodoList만 필터링
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({'date': '올바른 날짜 형식이 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(date=date)
            
            if queryset.exists():
                return queryset
            else:
                return []

        return queryset
        
    def list(self, request):
        queryset = self.get_queryset()
        serializer = TodoListSerializer(queryset, many=True, context={'request': request})
        # return Response(serializer.data[0])
        date_str = request.query_params.get('date')
        if date_str:
          if queryset:
              return Response(serializer.data[0])
          else:
              return Response([])
        else:
          return Response(serializer.data)


class TodoDateListView(generics.ListAPIView):
    def get_queryset(self):
        return TodoList.objects.exclude(todo_items=None).values_list('date', flat=True).distinct()

    def get(self, request):
        dates = self.get_queryset().dates('date', 'day', order='DESC')
        date_strings = [date.strftime('%Y-%m-%d') for date in dates]
        return Response(date_strings)


class TodoItemView(generics.UpdateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

    def put(self, request, *args, **kwargs):
        todo_item = get_object_or_404(self.queryset, id=kwargs['pk'])

        serializer = self.serializer_class(todo_item, data=request.data,  partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def delete(self, request, *args, **kwargs):
        todo_item = self.get_object()

        # todo_list = todo_item.todo_list
        todo_item.delete()

        # if todo_list.todo_items.count() == 0:
        #     TodoList.objects.filter(date=todo_list.date, todo_items__isnull=True).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
