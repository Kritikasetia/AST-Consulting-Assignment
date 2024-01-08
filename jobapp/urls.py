from django.urls import path
from .views import scraping, calculate_average_salary

urlpatterns = [
    path('scrape/', scraping, name='scraping'),
    path('average_salary/', calculate_average_salary, name='calculate_average_salary'),
]
