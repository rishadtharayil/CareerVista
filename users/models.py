from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model for CareerVista.
    """
    class Meta:
        db_table = 'auth_user' # Keep standard table name if preferred, or default
