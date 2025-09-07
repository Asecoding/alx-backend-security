# ip_tracking/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ip_tracking.models import SuspiciousIP
from django.core.cache import cache
from collections import defaultdict

SENSITIVE_PATHS = ['/admin', '/login']
THRESHOLD = 100  # requests/hour

@shared_task
def detect_suspicious_ips():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    # Simulated log structure: {ip: [(timestamp, path), ...]}
    request_logs = cache.get('request_logs', {})  # Replace with real log source

    flagged_ips = defaultdict(list)

    for ip, entries in request_logs.items():
        recent_entries = [entry for entry in entries if entry[0] >= one_hour_ago]

        if len(recent_entries) > THRESHOLD:
            flagged_ips[ip].append(f"Exceeded {THRESHOLD} requests/hour")

        if any(path in SENSITIVE_PATHS for _, path in recent_entries):
            flagged_ips[ip].append("Accessed sensitive paths")

    for ip, reasons in flagged_ips.items():
        SuspiciousIP.objects.update_or_create(
            ip_address=ip,
            defaults={'reason': "; ".join(reasons)}
        )

