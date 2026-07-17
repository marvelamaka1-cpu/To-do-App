from datetime import datetime, date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, TaskForm
from .models import Task


# ==========================================================
# Helper Functions
# ==========================================================

def get_greeting():
    """
    Returns greeting based on the current time.
    """

    hour = datetime.now().hour

    if hour < 12:
        return "Good Morning"

    elif hour < 18:
        return "Good Afternoon"

    elif hour < 21:
        return "Good Evening"

    return "Good Night"


def dashboard_statistics(tasks):
    """
    Calculate dashboard statistics.
    """

    total = tasks.count()

    completed = tasks.filter(done=True).count()

    pending = tasks.filter(done=False).count()

    progress = 0

    if total > 0:
        progress = round((completed / total) * 100)

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "progress": progress,
    }

@login_required(login_url="login")
def home(request):
    

    # Greeting
    greeting = f"{get_greeting()}, Marvelous!"

    # All tasks for the current user
    user_tasks = Task.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # ----------------------------------
    # Search
    # ----------------------------------

    search = request.GET.get("search", "")

    if search:

        user_tasks = user_tasks.filter(

            Q(title__icontains=search) |

            Q(description__icontains=search) |

            Q(category__icontains=search) |

            Q(priority__icontains=search)

        )

    # ----------------------------------
    # Dashboard Statistics
    # ----------------------------------

    stats = dashboard_statistics(

        Task.objects.filter(user=request.user)

    )

    total = stats["total"]

    completed = stats["completed"]

    pending = stats["pending"]

    progress = stats["progress"]

    # ----------------------------------
    # Extra Dashboard Cards
    # ----------------------------------

    today = date.today()

    today_tasks = Task.objects.filter(

        user=request.user,

        due_date=today

    ).count()

    high_priority = Task.objects.filter(

        user=request.user,

        priority="High"

    ).count()

    work_tasks = Task.objects.filter(
    user=request.user,
    category="Work"
    ).count()

    personal_tasks = Task.objects.filter(
    user=request.user,
    category="Personal"
    ).count()

    overdue_tasks = Task.objects.filter(

        user=request.user,

        done=False,

        due_date__lt=today

    ).count()

    # ----------------------------------
    # Pagination
    # ----------------------------------

    paginator = Paginator(

        user_tasks,

        8

    )

    page = request.GET.get("page")

    tasks = paginator.get_page(page)

    # ----------------------------------
    # Context
    # ----------------------------------

    context = {

        "greeting": greeting,

        "tasks": tasks,

        "search": search,

        # Main Stats
        "total": total,

        "completed": completed,

        "pending": pending,

        "progress": progress,

        # Charts
        "completed_chart": completed,

        "pending_chart": pending,

        # Extra Cards
        "today_tasks": today_tasks,

        "high_priority": high_priority,

        "business_tasks": work_tasks,

        "personal_tasks": personal_tasks,

        "overdue_tasks": overdue_tasks,

    }

    return render(request, "home.html")

# ==========================================================
# Authentication
# ==========================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm()

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                f"Welcome {user.username}! Your account has been created."
            )

            return redirect("home")

        messages.error(
            request,
            "Please correct the errors below."
        )

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )
    
    # ==========================================================
# Add Task
# ==========================================================

@login_required
def add_task(request):

    form = TaskForm()

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.user = request.user

            task.title = task.title.strip()

            if not task.title:

                messages.error(
                    request,
                    "Task title cannot be empty."
                )

                return redirect("add_task")

            duplicate = Task.objects.filter(
                user=request.user,
                title__iexact=task.title
            )

            if duplicate.exists():

                messages.warning(
                    request,
                    "A task with this title already exists."
                )

                return redirect("add_task")

            task.save()

            messages.success(
                request,
                "Task created successfully!"
            )

            return redirect("home")

    return render(
        request,
        "add_task.html",
        {
            "form": form
        }
    )


# ==========================================================
# Update Task
# ==========================================================

@login_required
def update_task(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    form = TaskForm(
        request.POST or None,
        instance=task
    )

    if request.method == "POST":

        if form.is_valid():

            updated = form.save(commit=False)

            updated.user = request.user

            updated.title = updated.title.strip()

            duplicate = Task.objects.filter(
                user=request.user,
                title__iexact=updated.title
            ).exclude(pk=task.pk)

            if duplicate.exists():

                messages.warning(
                    request,
                    "Another task already uses this title."
                )

                return redirect(
                    "update_task",
                    pk=pk
                )

            updated.save()

            messages.success(
                request,
                "Task updated successfully."
            )

            return redirect("home")

    return render(
        request,
        "update_task.html",
        {
            "form": form,
            "task": task
        }
    )


# ==========================================================
# Toggle Complete
# ==========================================================

@login_required
def toggle_task(request, task_id):

    task = get_object_or_404(
        Task,
        pk=task_id,
        user=request.user
    )

    task.done = not task.done

    task.save()

    if task.done:

        messages.success(
            request,
            f'"{task.title}" completed.'
        )

    else:

        messages.info(
            request,
            f'"{task.title}" marked as pending.'
        )

    return redirect("home")


# ==========================================================
# Delete Task
# ==========================================================

@login_required
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        pk=task_id,
        user=request.user
    )

    if request.method == "POST":

        title = task.title

        task.delete()

        messages.success(
            request,
            f'"{title}" deleted successfully.'
        )

    return redirect("home")


# ==========================================================
# Filter Tasks
# ==========================================================

@login_required
def filter_tasks(request, foo):

    tasks = Task.objects.filter(
        user=request.user
    )

    if foo == "true":

        tasks = tasks.filter(done=True)

    elif foo == "false":

        tasks = tasks.filter(done=False)

    tasks = tasks.order_by("-created_at")

    stats = dashboard_statistics(
        Task.objects.filter(user=request.user)
    )

    context = {

        "greeting": f"{get_greeting()}, Marvelous!",

        "tasks": tasks,

        "search": "",

        "total": stats["total"],

        "completed": stats["completed"],

        "pending": stats["pending"],

        "progress": stats["progress"],

        "completed_chart": stats["completed"],

        "pending_chart": stats["pending"],

        "today_tasks": Task.objects.filter(
            user=request.user,
            due_date=date.today()
        ).count(),

        "high_priority": Task.objects.filter(
            user=request.user,
            priority="High"
        ).count(),
        
        "business_tasks": Task.objects.filter(
        user=request.user,
        category="Work"
        ).count(),

        "personal_tasks": Task.objects.filter(
            user=request.user,
            category="Personal"
        ).count(),

        "overdue_tasks": Task.objects.filter(
            user=request.user,
            done=False,
            due_date__lt=date.today()
        ).count(),
    }

    return render(
        request,
        "home.html",
        context
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")