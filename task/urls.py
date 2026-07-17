from django.urls import path
from task.views import (
    home,
    add_task,
    filter_tasks,
    toggle_task,
    delete_task,
    update_task,
    login_view,
    register_view,
    logout_view,
)

urlpatterns = [

    path("", home, name="home"),

    path("add/", add_task, name="add_task"),

    path("tasks/<str:foo>/", filter_tasks, name="tasks"),

    path("toggle/<int:task_id>/", toggle_task, name="toggle_task"),

    path("delete/<int:task_id>/", delete_task, name="delete_task"),

    path("task/<int:pk>/", update_task, name="update_task"),

    path("login/", login_view, name="login"),

    path("register/", register_view, name="register"),

    path("logout/", logout_view, name="logout"),

]