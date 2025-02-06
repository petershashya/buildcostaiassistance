from django.shortcuts import render,redirect
from HouseCostApp.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages
def register_view(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        user_type = "user"

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        # Create the user
        user = CustomUser.objects.create(
            email=email,
            name=name,
            user_type=user_type,
            password=make_password(password)  # Encrypt the password
        )

        # Display success message
        messages.success(request, 'Registration successful. Please log in.')

        # Redirect to the login page
        return redirect('login')  # Assuming you have a named URL for login page

    return render(request, 'register.html')