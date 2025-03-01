from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# TODO: Import User model and any custom models needed

@login_required
def dashboard(request):
    """
    Display the appropriate dashboard based on user role
    """
    # TODO: Check if user is admin and redirect to admin dashboard if so
    user = request.user
    
    # TODO: Implement logic to check user role
    is_admin = user.is_staff  # Temporary implementation using is_staff
    
    if is_admin:
        return redirect('authentication:admin_dashboard')
    
    # Render regular user dashboard
    return render(request, 'authentication/dashboard.html')

@login_required
def admin_dashboard(request):
    """
    Display admin dashboard with additional functionality
    """
    # TODO: Check if user has admin privileges
    user = request.user
    
    if not user.is_staff:  # Temporary implementation using is_staff
        messages.error(request, "You don't have permission to access the admin dashboard.")
        return redirect('authentication:dashboard')
    
    # TODO: Retrieve data needed for admin dashboard
    
    return render(request, 'authentication/admin_dashboard.html')

# TODO: Implement password reset email customization if needed
# TODO: Implement user invitation system
# TODO: Implement user role management
