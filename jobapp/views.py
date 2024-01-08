from django.shortcuts import render
from django.http import HttpResponse
from .models import Job
from pymongo.errors import DuplicateKeyError
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient
import re
from django.shortcuts import render
from .models import Job
import numpy as np
# setup for web viewing
def get_driver(link):
    driver = webdriver.Chrome()
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    return soup

# finding all the jobs and storing their info in the database
def scraping(request):
    # Connect to MongoDB (Make sure your MongoDB server is running)
    client = MongoClient("mongodb://localhost:27017/")
    database = client["scrapeddata"]
    collection = database["jobapp_job"]

    # Put the number of pages * 10 in place of the second int in the for loop
    for i in range(0, 100, 10):
        page_html = get_driver(
            f"https://in.indeed.com/jobs?q=python+developer&l=Noida%2C+Uttar+Pradesh&start={i}&vjk=74df27615b32ca3c")
        scraping_page(page_html, collection)

    return render(request, 'jobapp/scrape_success.html')

def scraping_page(page, collection):
    jobs = page.find_all("div", class_="job_seen_beacon")
    for job in jobs:
        company_name = job.find("span", class_="css-1x7z1ps eu4oa1w0").text
        company_location = job.find("div", class_="css-t4u72d eu4oa1w0").text

        try:
            salary = job.find("div", class_="metadata salary-snippet-container").text
            salary_list = salary.split('-')
            for i in range(len(salary_list)):
                salary_list[i] = re.sub(r'[^\d$.,]', '', salary_list[i])
            if len(salary_list) == 2:
                min_salary = salary_list[0]
                max_salary = salary_list[1]
            else:
                min_salary = salary_list[0]
                max_salary = None
        except:
            min_salary = "click link to find"
            max_salary = None

        job_title = job.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0").text

        link_tag = job.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0")
        link_half = link_tag["href"]
        base_url = "https://in.indeed.com"
        full_url = f"{base_url}{link_half}"

        job_info = {
            "job_title": job_title,
            "salary_min": min_salary,
            "salary_max": max_salary,
            "company_name": company_name,
            "company_location": company_location,
            "link": full_url
        }

        # Insert job information into MongoDB
        #job=Job()
        Job.objects.create(
            job_title=job_info["job_title"],
            salary_min=job_info["salary_min"],
            salary_max=job_info["salary_max"],
            company_name=job_info["company_name"],
            company_location=job_info["company_location"],
            link=job_info["link"]
        )

        #update_data= {'$set': job_info}
        #collection.update_one(job_info,update_data,upsert=True)
def calculate_average_salary(request):

    python_jobs = Job.objects.filter(job_title__icontains='Python Developer', company_location__icontains='Noida, Uttar Pradesh')

    salaries = []
    for job in python_jobs:

        if job.salary_min is not None:
            min_salary = job.salary_min.replace(',', '')
        else:
            min_salary=None
        if job.salary_max is not None:
            max_salary = job.salary_max.replace(',', '')
        else:
            max_salary= None

        try:
            min_salary = float(min_salary)
        except ValueError:
            min_salary = None

        try:
            max_salary = float(max_salary)
        except Exception:
            max_salary = None

        # Add valid salaries to the list
        if min_salary is not None:
            salaries.append(min_salary)
        if max_salary is not None:
            salaries.append(max_salary)


    average_salary = np.mean(salaries) if salaries else 0

    return render(request, 'jobapp/average_salary.html', {'average_salary': average_salary})
