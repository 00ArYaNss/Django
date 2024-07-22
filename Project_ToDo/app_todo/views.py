from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem

def index(request):
    todos = TodoItem.objects.all()
    return render(request, 'index.html', {'todos': todos})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        TodoItem.objects.create(title=title, description=description)
        return redirect('index')
    return render(request, 'add_task.html')

def edit_task(request, task_id):
    todo = get_object_or_404(TodoItem, id=task_id)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        todo.completed = 'completed' in request.POST
        todo.save()
        return redirect('index')
    return render(request, 'edit_task.html', {'todo': todo})

def delete_task(request, task_id):
    todo = get_object_or_404(TodoItem, id=task_id)
    todo.delete()
    return redirect('index')

def operations(request):
    return render(request, 'operations.html')
