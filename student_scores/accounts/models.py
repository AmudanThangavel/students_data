from django.db import models
from django.db import models
# Create your models here.


class students_data(models.Models):
    name = models.CharField(max_length=30)
    roll_no = models.CharField(max_length=10)
    department = models.CharField(max_length=35)
    score = models.DecimalField()
    team_no = models.IntegerField()