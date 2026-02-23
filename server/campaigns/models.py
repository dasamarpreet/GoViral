from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from datetime import timedelta


def default_deadline():
    return timezone.now() + timedelta(hours=48)


class Campaign(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        LIVE = "LIVE", "Live"
        CLOSED = "CLOSED", "Closed"

    PLATFORM_CHOICES = [
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("x", "X (Twitter)"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
    ]

    company = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaigns"
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    platform = ArrayField(
        models.CharField(max_length=50, choices=PLATFORM_CHOICES),
        blank=True,
        default=list
    )

    price_per_k_view = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1_00_000
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    deadline_to_bid = models.DateTimeField(default=default_deadline)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

