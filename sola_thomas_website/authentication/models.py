from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extension of the User model to add additional information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_admin = models.BooleanField(default=False)
    # TODO: Add additional fields as needed
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Invitation(models.Model):
    """
    Model to manage user invitations
    """
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # TODO: Add method to send invitation email
    def send_invitation(self):
        """Send invitation email with registration link"""
        pass
    
    def __str__(self):
        return f"Invitation for {self.email}"
