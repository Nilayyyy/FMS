from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AddSpending(models.Model):
    FMSuser=models.CharField(max_length=20)
    PaidTo=models.CharField(max_length=122)
    Amount=models.DecimalField(max_digits=10, decimal_places=2)
    # TransactionID=models.CharField(max_length=122, default="")
    Date=models.DateField()
    Reason=models.CharField(max_length=50)
    Remarks=models.CharField(max_length=122)
    
