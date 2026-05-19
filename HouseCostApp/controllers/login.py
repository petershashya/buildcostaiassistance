from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            if user.is_superuser:
                return redirect('admin-page')  # Redirect to admin page if superuser
            return redirect('scan_house_map')  # Assuming you have a named URL for the home page
        else:
            # Authentication failed, display error message
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')