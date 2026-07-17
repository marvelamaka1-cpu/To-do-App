from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator


class Task(models.Model):

    PRIORITY_CHOICES = (
        ("High", "High 🔴"),
        ("Medium", "Medium 🟡"),
        ("Low", "Low 🟢"),
    )


    CATEGORY_CHOICES = (
        ("Business", "💼 Business"),
        ("School", "📚 School"),
        ("Personal", "👤 Personal"),
        ("Shopping", "🛒 Shopping"),
        ("Health", "❤️ Health"),
        ("Others", "📌 Others"),
    )


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )


    title = models.CharField(
        max_length=140,
        validators=[
            MinLengthValidator(
                3,
                "Task title must contain at least 3 characters."
            )
        ]
    )


    description = models.TextField(
    blank=True,
    default=""
)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="Personal"
    )


    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )


    done = models.BooleanField(
        default=False
    )


    due_date = models.DateField(
        blank=True,
        null=True
    )


    due_time = models.TimeField(
        blank=True,
        null=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )



    @property
    def is_overdue(self):

        if self.done:
            return False


        if self.due_date:

            return (
                self.due_date <
                timezone.now().date()
            )


        return False



    @property
    def due_datetime(self):

        """
        Combines due date and due time.
        """

        if self.due_date:

            if self.due_time:

                return timezone.datetime.combine(
                    self.due_date,
                    self.due_time
                )

            return timezone.datetime.combine(
                self.due_date,
                timezone.datetime.min.time()
            )

        return None



    def mark_completed(self):

        """
        Marks task as completed.
        """

        self.done = True
        self.completed_at = timezone.now()

        self.save()



    class Meta:

        ordering = [
            "-created_at"
        ]


        indexes = [

            models.Index(
                fields=[
                    "user",
                    "done"
                ]
            ),

            models.Index(
                fields=[
                    "user",
                    "category"
                ]
            ),

            models.Index(
                fields=[
                    "user",
                    "priority"
                ]
            ),

            models.Index(
                fields=[
                    "due_date"
                ]
            ),
        ]



    def __str__(self):

        return f"{self.title} - {self.user.username}"