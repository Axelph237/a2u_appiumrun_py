import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

# Create your views here.

@csrf_exempt
def start_appium(request):
    try:
        subprocess.Popen(['appium.cmd'])
        print(os.getenv('APPIUM_SERVER_URL'))
        return JsonResponse({'status': 'Appium server started successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def stop_appium(request):
    try:
        #subprocess.Popen(['pkill', '-f', 'appium'])
        return JsonResponse({'status': 'Appium server stopped successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def run_appium_test(request):
    try:
        # Replace with your actual test command
        subprocess.Popen(['python', 'a2u_appiumrun\\tests\\example_test.py'])
        return JsonResponse({'status': 'Appium test started successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
