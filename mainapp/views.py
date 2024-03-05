from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from flask import request, Flask

from .models import *
from django.contrib.auth import logout

from django.shortcuts import render
from django.http import HttpResponse
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Create your views here.
def myfunction(request):
    return render(request, "mainpage.html")
def myabout(request):
    return render(request, "about.html")
def myabout1(request):
    return render(request, "about1.html")
def mylogin(request):
    return render(request, "login.html")
def myregistration(request):
    return render(request, "registration.html")
def mycontact(request):
    return render(request, "contact.html")
def mycontact1(request):
    return render(request, "contact1.html")
def adminhome(request):
    return render(request, "adminhomepage.html")
def userhome(request):
    return render(request, "userhomepage.html")

def registration_view(request):
    user_exists = False
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        phone = request.POST['phone']
        if User.objects.filter(email=email).exists():
            messages.info(request, 'User with this email already exists. Please log in.')
            return render(request, 'login.html')
        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        messages.info(request, 'Account created Successfully!')
        return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.get(username=username)
        if user.check_password(password):
            # If username and password match, redirect to admin page
            if username == 'admin@gmail.com' and password == 'admin':
                return render(request, 'adminhomepage.html') # Assuming the URL name for the admin page is 'admin_page'
            else:
                return  render(request, 'userhomepage.html')  # Assuming the URL name for the user page is 'user_page'
        else:
            # If password does not match, display a message
            messages.info(request, 'Invalid password. Please try again')
            return render(request, 'login.html')


def show_topplaces(request):
    topplaces = Topplaces.objects.all()
    return render(request, 'show_topplaces.html', {'topplaces': topplaces})
def show_tophotels(request):
    tophotels = Tophotels.objects.all()
    return render(request, 'show_tophotels.html', {'tophotels': tophotels})

def show_tophotels1(request):
    tophotels1 = Tophotels.objects.all()
    query = request.GET.get('place')
    if query:
        tophotels1 = tophotels1.filter(place__icontains=query)
    return render(request, 'show_tophotels.html', {'tophotels1': tophotels1})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('main')

app = Flask(__name__)

# Weather API configuration
weather_api_key = 'your_weather_api_key'
weather_api_url = 'http://api.openweathermap.org/data/2.5/weather'

# Email configuration
email_address = 'deekshithatadepallil@example.com'
email_password = 'Tadepalli@143'
reciever_email = '2200031434@kluniversity.in'


def fetch_weather_data(city, params=None):
    params = params or {}
    params['q'] = city
    params['appid'] = weather_api_key
    response = requests.get(weather_api_url, params=params)
    print("API Response Status Code:", response.status_code)
    print("API Response Content:", response.content)
    data = response.json()
    return data
def send_email(receiver_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    text = msg.as_string()
    server.sendmail(email_address, receiver_email, text)

    server.quit()

def get_weather(request):
    if request.method == 'POST':
        data = request.POST
        city = data.get('city')
        if not city:
            return HttpResponse("City name is required.", status=400)

        weather_data = fetch_weather_data(city)

        # Print weather data for debugging
        print("Weather Data:", weather_data)

        if not weather_data:
            return HttpResponse("Failed to fetch weather data.", status=500)

        try:
            temperature = weather_data['main']['temp']
            weather_desc = weather_data['weather'][0]['description']
        except KeyError as e:
            print("Failed to parse weather data:", e)
            return HttpResponse("Failed to parse weather data.", status=500)

        receiver_email = data.get('email')
        if not receiver_email:
            return HttpResponse("Email address is required.", status=400)

        subject = f"Weather Report for {city}"
        body = f"The temperature in {city} is {temperature}°C with {weather_desc}."
        send_email(receiver_email, subject, body)

        # Redirect the user to another page or the same page with a success message
        return redirect('success_page')
    else:
        return render(request, 'weather.html')

def success_page(request):
    return render(request, 'success_page.html')
if __name__ == '__main__':
    app.run(debug=True)