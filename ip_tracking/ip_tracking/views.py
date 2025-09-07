# ip_tracking/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit

@csrf_exempt
@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    # Your login logic here
    return JsonResponse({'message': 'Login attempt received'})

