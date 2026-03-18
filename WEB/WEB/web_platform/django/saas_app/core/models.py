from __future__ import annotations

from django.conf import settings
from django.db import models


class Org(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Subscription(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    plan_key = models.CharField(max_length=50, default="free")
    active = models.BooleanField(default=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.org}::{self.plan_key}"


class ApiKey(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    key_prefix = models.CharField(max_length=16)
    key_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.org}::{self.key_prefix}"


class AuditLog(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, null=True, blank=True)
    actor_user_id = models.IntegerField(null=True, blank=True)
    event = models.CharField(max_length=200)
    payload = models.TextField(default="{}")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.event


