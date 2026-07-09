# from django.shortcuts import render, redirect, get_object_or_404
# import datetime
# from .models import Task
# from .forms import TaskForm


# def home(request):
#     date = datetime.datetime.now()
#     h = int(date.strftime('%H'))

#     if h < 12:
#         time_of_day = "Morning"
#     elif h < 18:
#         time_of_day = "Afternoon"
#     elif h < 21:
#         time_of_day = "Evening"
#     else:
#         time_of_day = "Night"

#     greeting = f"Good {time_of_day}, Marvelous!"

#     tasks = Task.objects.all().order_by("-created_at")

#     context = {
#         "greeting": greeting,
#         "tasks": tasks,
#     }

#     return render(request, "home.html", context)


# def add_task(request):
#     print("ADD TASK VIEW CALLED")

#     forms = TaskForm()
    
#     if request.method == "POST":
#         forms = TaskForm(request.POST)
#         #====================================
#         # Check for validation
#         # ====================================
        
#         if forms.is_valid():
#             forms.save()
#             return redirect('home')
#         else:
#             return redirect('add_task')
#     context = {
#         'forms' : forms
#     }

#     # if request.method == "POST":
#     #     title = request.POST.get("title", "").strip()
#     #     print(title)
#     #     due_time = request.POST.get('due_time')
        
#     #     task = Task.objects.create(
#     #         title =title,
#     #         due_time =due_time
#     #     )

#     #     task.save()

#     return render(request, 'add_task.html', context)

    

# def filter_tasks(request, foo):
#     if foo == "true":
#         tasks = Task.objects.filter(done=True)
#     elif foo == "false":
#         tasks = Task.objects.filter(done=False)
#     else:
#         tasks = Task.objects.all().order_by('-created_at')

#     date = datetime.datetime.now()
#     h = int(date.strftime("%H"))

#     if h < 12:
#         time_of_day = "Morning"
#     elif h < 18:
#         time_of_day = "Afternoon"
#     elif h < 21:
#         time_of_day = "Evening"
#     else:
#         time_of_day = "Night"

#     greeting = f"Good {time_of_day}, Marvelous!"

#     context = {
#         "tasks": tasks,
#         "greeting": greeting,
#     }

#     return render(request, "home.html", context)


# def update_task(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     form = TaskForm(instance=task)
#     task = Task.objects.get(id=pk)

#     if request.method == "POST":
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
            
        
#             return redirect('task, pk=pk')

#     context = {
#         "task": task,
#     }

#     return render(request, "update_task.html", context)



# def toggle_task(request, task_id):
#     task = get_object_or_404(Task, pk=task_id)
#     task.done = not task.done
#     task.save()

#     return redirect("home")


# def delete_task(request, task_id):
#         task = get_object_or_404(Task, pk=task_id)
#         task.delete()

#         return redirect("home")

# def login(request):
#     return render(request, "login.html")

from django.shortcuts import render, redirect, get_object_or_404
import datetime
from .models import Task
from .forms import TaskForm


def home(request):
    date = datetime.datetime.now()
    h = int(date.strftime('%H'))

    if h < 12:
        time_of_day = "Morning"
    elif h < 18:
        time_of_day = "Afternoon"
    elif h < 21:
        time_of_day = "Evening"
    else:
        time_of_day = "Night"

    greeting = f"Good {time_of_day}, Marvelous!"

    tasks = Task.objects.all().order_by("-created_at")

    context = {
        "greeting": greeting,
        "tasks": tasks,
    }

    return render(request, "home.html", context)


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TaskForm()

    context = {
        "form": form,
    }

    return render(request, "add_task.html", context)


def filter_tasks(request, foo):
    if foo == "true":
        tasks = Task.objects.filter(done=True)
    elif foo == "false":
        tasks = Task.objects.filter(done=False)
    else:
        tasks = Task.objects.all().order_by("-created_at")

    date = datetime.datetime.now()
    h = int(date.strftime("%H"))

    if h < 12:
        time_of_day = "Morning"
    elif h < 18:
        time_of_day = "Afternoon"
    elif h < 21:
        time_of_day = "Evening"
    else:
        time_of_day = "Night"

    greeting = f"Good {time_of_day}, Marvelous!"

    context = {
        "tasks": tasks,
        "greeting": greeting,
    }

    return render(request, "home.html", context)


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TaskForm(instance=task)

    context = {
        "form": form,
    }

    return render(request, "update_task.html", context)


def toggle_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.done = not task.done
    task.save()

    return redirect("home")


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()

    return redirect("home")


def login(request):
    return render(request, "login.html")  