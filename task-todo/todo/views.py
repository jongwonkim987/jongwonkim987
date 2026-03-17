from django.shortcuts import render
from django.http import Http404
from todo.models import Todo

def todo_list(request):
    todo_list = Todo.objects.all().values_list('id', 'titile')
    result = []
    for todo in todo_list:
        result.append({'id': todo[0], 'title': todo[1]})

    return render(request, 'todo_list.html', {'data': result})

def todo_info(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        info = {
            'title': todo.title,
            'description': todo.description,
            'start_date': todo.start_date,
            'end_date': todo.end_date,
            'is_completed': todo.is_completed,
        }
        return render(request, 'todo_info.html', {'data': info})
    except:
        raise Http404