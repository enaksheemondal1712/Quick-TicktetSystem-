from django.db import models


class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ("General", "General"),
        ("Billing", "Billing"),
        ("Technical", "Technical"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("Closed", "Closed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
