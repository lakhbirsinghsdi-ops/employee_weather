from django.shortcuts import render, redirect
from .models import Employee
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
import requests
from django.conf import settings
data = get_user_model()

def sign_up(request):
    if request.method == "POST":
        user = request.POST.get("name")
        mobile = request.POST.get("phon")
        password = request.POST.get("password")
        confirm = request.POST.get("cpassword")
        ab = data.objects.all()
        b = [i.username for i in ab]
        if user not in b:
            if password == confirm:
                a = data(username=user, phone_number=mobile, password=make_password(password))
                a.save()
                return redirect("../login")
            else:
                return render(request, "pages/signup.html", {"message": "password and confirm password is not match"})
        else:
            return render(request, "pages/signup.html", {"message1": "username already exists"})
    return render(request, "pages/signup.html")

def log_in(request):
    if request.method == "POST":
        name = request.POST.get("n")
        password = request.POST.get("p")
        num = authenticate(username=name, password=password)
        ab = data.objects.all()
        b = [i.username for i in ab]

        if name in b:
            if num is not None:
                request.session["xyz"] = name
                return redirect("../dash")
            else:
                return render(request, "pages/login.html", {"message": "username and password is not correct"})
        else:
            return render(request, "pages/login.html", {"message1": "username is not exists, firstly enter yourself"})
    return render(request, "pages/login.html")

def dashboard(request):
    total_employees = Employee.objects.count()
    cities = ["Delhi", "Chandigarh", "Mohali", "Zirakpur", "Panchkula", "Mumbai", "Bengaluru"]
    selected_city = request.GET.get("city", "Delhi")
    api_key = settings.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") != 200:
        weather = {"error": "Unable to fetch weather data."}
    else:
        weather = {
            "city": response["name"],
            "country": response["sys"]["country"],
            "temperature": response["main"]["temp"],
            "feels_like": response["main"]["feels_like"],
            "humidity": response["main"]["humidity"],
            "pressure": response["main"]["pressure"],
            "description": response["weather"][0]["description"].title(),
            "icon": response["weather"][0]["icon"],
            "wind_speed": response["wind"]["speed"],
        }

    return render(request, "pages/dashboard.html", {
        "Total_Employees": total_employees,
        "weather": weather,
        "cities": cities,
        "selected_city": selected_city,
    })

def employee_list(request):
    a = data.objects.all()
    dat = []

    for i in a:
        print(i.designation)
        dat.append({
            "username": i.username,
            "salary": i.salary,
            "designation":i.designation,
            "id":i.id
        })
    paginator = Paginator(dat, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,"pages/employee_list.html",{"page_obj": page_obj})
def employee_add(request):
    if request.method == "POST":
        email = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm = request.POST.get('cpassword')
        designation = request.POST.get('designation')
        salary = request.POST.get('salary')
        print("kjhghjs")
        if password==confirm:
            print("jhgfghujyhg")
            emp = data(username=email,phone_number=phone,
                       password=password,designation=designation,
                       salary=salary)
            emp.save()
            return redirect('../')
        else:       
            return render(request,"pages/employee_form.html",
                          {'message':"password or confirm password didnot matched"})
    return render(request,"pages/employee_form.html")
def log_out(request):
    if "xyz" in request.session:
        del request.session["xyz"]
    return redirect("../login")

def employee_delete(request,id):
    obj = data.objects.get(id=id)
    obj.delete()
    return redirect("employee_list")
def employee_edit(request,id):
    print(id)
    username = request.POST.get("username")
    designation = request.POST.get("designation")
    salary = request.POST.get("salary")
    obj = data.objects.get(id=id)
    obj.username = username
    obj.designation = designation
    obj.salary = salary
    obj.save()

    return redirect("employee_list")