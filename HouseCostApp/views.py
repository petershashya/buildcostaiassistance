from django.shortcuts import render,redirect

from HouseCostApp.models import House
from .controllers.login import login_view
from .controllers.register import register_view
from .controllers.user import history_view,predict,prediction,historyview
from django.contrib.auth import logout
from .controllers.admin import admin_page,admin_report,admin_users
from django.contrib import messages
from django.contrib.auth import get_user_model

def index(request):
    return render(request, 'index.html')
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

def house_list(request):
 
    houses = House.objects.select_related('user').all() 
    return render(request, 'admin_history.html', {'houses': houses})

def admin_history(request):
    return render(request, 'admin_history.html')

def loader_view(request):
    return render(request, 'layouts/loader.html')



User = get_user_model()

# deleting function

def delete_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(pk=user_id)
        user.delete()
        return redirect('admin-users')  # Redirect to a relevant page after deletion
    else:
        # Handle GET request or other methods as needed
        pass
# Create your views here.
