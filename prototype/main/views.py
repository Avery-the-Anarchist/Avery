from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import FavoritedProducts, Products, Users, Posts
import json
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
import requests
from django.core.paginator import Paginator
import datetime
from django.contrib import messages


def index(request):
    post_list = Posts.objects.all()
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'dashboard.html', {'posts':posts})

def apigrabber(request):
       # grabbing stuffs from API into database if they're not there already
    response = requests.get("https://fakestoreapi.com/products/category/men's clothing")
    data = response.json()
    for p in data:
        if not Products.objects.filter(productname=p['title'], price=p['price'], image=p['image'], category=p['category']):
            b = Products(productname=p['title'], price=p['price'], image=p['image'], category=p['category'])
            b.save()

    response = requests.get("https://fakestoreapi.com/products/category/women's clothing")
    data = response.json()
    for p in data:
        if not Products.objects.filter(productname=p['title'], price=p['price'], image=p['image'], category=p['category']):
            b = Products(productname=p['title'], price=p['price'], image=p['image'], category=p['category'])
            b.save()
    return render(request, 'index.html')

def get_favorite(request,userid):
    response=list(FavoritedProducts.objects.filter(userid=userid).values('productid'))
    return JsonResponse(response, content_type='application/json', safe=False)

def change_favorite(request,userid, productid):
    count = FavoritedProducts.objects.filter(productid=productid,userid=userid).count()
    if (count > 0):
         FavoritedProducts.objects.filter(productid=productid,userid=userid).delete()
    else:
         user = Users.objects.get(userid=userid)
         product = Products.objects.get(productid=productid)
         FavoritedProducts.objects.create(productid=product,userid=user,date=datetime.datetime.now())

    return JsonResponse(productid, content_type='application/json', safe=False)


def marketplace(request):
 
    

    search_query = request.GET.get('search', '')
    if search_query:
        product_list = Products.objects.filter(productname__icontains=search_query)
    else:
        product_list = Products.objects.all()

    tag = request.GET.get('tag', '')
    if tag:
        product_list = product_list.filter(tags__name__in=[tag])

    

    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'marketplace.html', {'products':products})


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            # Create User in Django built-in User model
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect('main:signup')  # No .html
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('main:signup')  # No .html
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                # Create the actual User profile that would be saved in our own database
                user_object = User.objects.get(username=username)
                new_user = Users.objects.create(
                    username=user_object.username, 
                    userid=user_object.id, 
                    password=user_object.password, 
                    email=user_object.email
                )
                new_user.save()

                messages.info(request, 'User created')
                return redirect('main:signup')  # Optionally redirect to login instead of signup

        else:
            messages.info(request, 'Passwords do not match')
            return redirect('main:signup')  # No .html

    return render(request, 'signup.html') 

def signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=auth.authenticate(username=username, password=password) # check if a user with this info exists
        if user is not None:  #log in if exsits and return to home page
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid login")
            return redirect("main:signin")

    else:
        return render(request, "signin.html")
    

def logout(request):
    auth.logout(request)
    return redirect("main:signin")