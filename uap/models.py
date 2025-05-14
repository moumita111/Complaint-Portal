from django.db import models
from django.contrib.auth.models import User


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
# Create your models here.



