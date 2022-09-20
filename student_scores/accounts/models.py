from django.db import models
# Create your models here.


class students_data(models.Model):
    name = models.CharField(max_length=30)
    roll_no = models.CharField(max_length=10)
    department = models.CharField(max_length=35)
    score = models.DecimalField(max_digits=10, decimal_places=3)
    team_no = models.IntegerField()

    def __str__(self):
        return self.roll_no
