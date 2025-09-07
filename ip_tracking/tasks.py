from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ["/admin", "/login"]

@shared_task
def detect_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Get recent logs
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # Count requests per IP
    ip_request_counts = {}
    for log in logs:
        ip_request_counts[log.ip_address] = ip_request_counts.get(log.ip_address, 0) + 1

        # Rule 1: Sensitive paths
        if log.path in SENSITIVE_PATHS:
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                reason=f"Accessed sensitive path: {log.path}",
            )

    # Rule 2: More than 100 requests/hour
    for ip, count in ip_request_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason=f"Exceeded 100 requests in the last hour ({count})",
            )