import os
import json
import psutil
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from a2u_appiumrun.data_handlers import test_handler as th


appiumProc = None


# Create your views here.
@csrf_exempt
def tests(request):
    try:
        if request.method == 'GET':
            # Handle GET request
            if th.initialized:
                return JsonResponse(th.definitions, safe=False)

            raise ValueError('Tests have not been initialized.')

        if request.method == 'POST':
            # Handle POST request
            pass

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def start_appium(request):
    try:
        global appiumProc
        appiumProc = subprocess.Popen(['appium.cmd'])

        return JsonResponse({'status': 'Appium server started successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def stop_appium(request):
    try:
        if appiumProc is not None:
            kill(appiumProc.pid)
            # communication required to perform kill function
            outs, errs = appiumProc.communicate()
        else:
            raise TypeError('Appium has not been started')
        return JsonResponse({'status': 'Appium server stopped successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def run_appium_test(request):
    try:
        # Replace with your actual test command
        venv_python = os.path.join(os.getcwd(), 'venv', 'Scripts', 'python.exe')
        script_path = os.path.join(os.getcwd(), 'a2u_appiumrun', 'tests', 'appium_test_file.py')

        data = {"input1": "value1"}
        data_str = json.dumps(data)

        test = subprocess.run([venv_python, script_path, data_str], capture_output=True, text=True)

        if test.stdout != '':
            print("The subprocess produced the following output:\n" + test.stdout)
        if test.stderr != '':
            print("Errors found in subprocess:\n" + test.stderr)
        return JsonResponse({'status': 'Appium test completed',
                             'returncode': test.returncode,
                             'output': test.stdout,
                             'errors': test.stderr})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# kills a subprocess and all of its child processes
def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()
