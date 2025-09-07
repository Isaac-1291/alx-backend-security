from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

# Authenticated users: 10 requests per minute
# Anonymous users: 5 requests per minute

@csrf_exempt
@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=False)
@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def login_view(request):
    # If request is limited, return 429
    if getattr(request, 'limited', False):
        return HttpResponse("Too many requests", status=429)

    if request.method == "POST":
        # Process login attempt
        return HttpResponse("Login attempt processed")

    # Show login page
    return HttpResponse("Login page")