from django.contrib import admin
from accounts.models import students_data
# Register your models here.


class StudentsDataAdmin(students_data):
    list_filter = ('roll_no', 'team_no', 'score')
    list_display = ('name', 'roll_no', 'score', 'team_no')


# admin.site.register(students_data)
admin.site.register(students_data, StudentsDataAdmin)
