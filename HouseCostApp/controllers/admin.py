from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from HouseCostApp.models import CustomUser,House
def admin_page(request):
    user_count = CustomUser.objects.count() 
    transactions=House.objects.count()
    # Get the count of all users
    context = {
        'user_count': user_count,
        'transactions':transactions
        
    }
    return render(request, ['admin-page.html', 'admin_history.html'], context=context)
# Register your models here.
def admin_users(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
        
    }
    return render(request,'admin-users.html',context)
def admin_report(request):
    return render(request,'admin-report.html')

 # Replace 'some_view_name' with the name of the view you want to redirect to after deletion