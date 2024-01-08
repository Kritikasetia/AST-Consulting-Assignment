from django.contrib import admin

# Register your models here.
# jobapp/admin.py
# jobapp/admin.py
from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'company_name', 'company_location', 'link', 'salary_min', 'salary_max')
    search_fields = ['job_title', 'company_name', 'company_location']

admin.site.register(Job, JobAdmin)



