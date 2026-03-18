from __future__ import annotations

from django.contrib import admin

from .models import ApiKey, AuditLog, Org, Subscription


admin.site.register(Org)
admin.site.register(Subscription)
admin.site.register(ApiKey)
admin.site.register(AuditLog)

