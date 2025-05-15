from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    semester = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username



class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='complaints/', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=False)
    total_upvotes = models.IntegerField(default=0)
    total_downvotes = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)

    def __str__(self):
        if self.is_anonymous:
            return f"Anonymous Complaint - {self.title} ({self.status})"
        return f"{self.user.username} - {self.title} ({self.status})"

    def get_display_user(self, is_admin=False):
        """Return username depending on anonymity and whether viewer is admin."""
        if self.user:
            if self.is_anonymous and not is_admin:
                return "Anonymous"
            return self.user.username
        return "No User Assigned"
    


class Authority(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"Faculty: {self.user.username} - {self.department}"

class ComplaintResponse(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="responses")
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.authority.user.username} on {self.complaint.title}"


class Feedback(models.Model):
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Feedback by {self.user.username} - {self.rating}/5"
    

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



