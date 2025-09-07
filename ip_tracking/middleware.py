from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
import ipinfo
from django.core.cache import cache
import os

# Use your IPinfo API token
IPINFO_TOKEN = os.getenv("IPINFO_API_TOKEN", "your_api_token_here")
ipinfo_handler = ipinfo.getHandler(IPINFO_TOKEN)

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

# Fetch geolocation from cache or API
        geo_data = cache.get(ip)
        if not geo_data:
            try:
                details = ipinfo_handler.getDetails(ip)
                geo_data = {
                    "country": details.country_name,
                    "city": details.city
                }
            except Exception:
                geo_data = {"country": None, "city": None}
            cache.set(ip, geo_data, 86400)  # Cache 24h

        # Log the request
        RequestLog.objects.create(ip_address=ip, path=request.path,
        country=geo_data.get("country"),
            city=geo_data.get("city")
        )
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
