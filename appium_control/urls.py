from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.tests, name='tests'),
    path('start_appium/', views.start_appium, name='start_appium'),
    path('stop_appium/', views.stop_appium, name='stop_appium'),
    path('run_appium_test/', views.run_appium_test, name='run_appium_test'),
    path('read_test_requirements/', views.read_test_requirements, name='read_test_requirements'),
]