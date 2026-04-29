from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField, Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from rest_framework.decorators import api_view

from .models import StudyTask
from .forms import StudyTaskForm
from .serializers import StudyTaskSerializer

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'planner/register.html', {'form': form})

@login_required
def dashboard(request):
    tasks = StudyTask.objects.filter(user=request.user).annotate(
        priority_order=Case(
            When(priority='High', then=Value(0)),
            When(priority='Medium', then=Value(1)),
            When(priority='Low', then=Value(2)),
            output_field=IntegerField(),
        )
    ).order_by('is_completed', 'priority_order', 'due_date')
    
    pending_hours = StudyTask.objects.filter(user=request.user, is_completed=False).aggregate(total_time=Sum('estimated_time'))['total_time'] or 0
    pending_hours = round(pending_hours / 60, 1)

    subjects = StudyTask.objects.filter(user=request.user).values_list('subject', flat=True).distinct()

    return render(request, 'planner/dashboard.html', {
        'tasks': tasks,
        'pending_hours': pending_hours,
        'subjects': subjects
    })

@login_required
def add_task(request):
    if request.method == 'POST':
        form = StudyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = StudyTaskForm()
    return render(request, 'planner/task_form.html', {'form': form, 'title': 'Add New Study Task'})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)
    if request.method == 'POST':
        form = StudyTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudyTaskForm(instance=task)
    return render(request, 'planner/task_form.html', {'form': form, 'title': 'Edit Study Task'})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)
    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect('dashboard')

@login_required
@require_POST
def toggle_task_completion(request, task_id):
    try:
        task = StudyTask.objects.get(id=task_id, user=request.user)
        task.is_completed = not task.is_completed
        task.save()
        return JsonResponse({'status': 'success', 'is_completed': task.is_completed})
    except StudyTask.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)

@login_required
def reset_planner(request):
    StudyTask.objects.filter(user=request.user, is_completed=True).delete()
    messages.success(request, "Completed tasks have been successfully removed.")
    return redirect('dashboard')

@api_view(['GET'])
def task_list_api(request):
    tasks = StudyTask.objects.filter(user=request.user)
    serializer = StudyTaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)
