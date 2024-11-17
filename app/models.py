from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class resetuuid(models.Model):
    UUID = models.UUIDField(unique=True, editable=False)
    user = models.ForeignKey(to = User, on_delete= models.CASCADE)
    expiry = models.DateTimeField()  
    is_session_expired = models.BooleanField(default=False)