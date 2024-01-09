# AST-Consulting-Assignment

Step 1 Python Enivronement Setup
pip install virtualenv 
python -m venv myenv
myenv\Scripts\activate

Step 2 Install dependencies
pip install -r requirements.txt

Step 3 Mondodb credentials
In jobapp directory
In views.py write the name of your database and collection name
In settings.py in Database ={Name :write the name of your mongodb database

Step 4 Run Migration
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser # helps in login for django admin panel

Step 5 Run server
python manage.py runserver
This will start the server at  http://127.0.0.1:8000/
to scrape click on url :http://127.0.0.1:8000/jobs/scrape
to compute the average:http://127.0.0.1:8000/jobs/average_salary/
to open admin panel :http://127.0.0.1:8000/admin/

Screenshot of admin panel:
![image](https://github.com/Kritikasetia/AST-Consulting-Assignment/assets/79091276/960afa6e-a0a3-4ecb-81ec-bbb6ddcef411)


 
