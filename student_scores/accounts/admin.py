from django.contrib import admin
from accounts.models import students_data
# Register your models here.
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class StudentResource(resources.ModelResource):

    class Meta:
        model = students_data
        import_id_fields = ('roll_no',)
        # exclude = ('id', )
        # fields = ('id','text','option1','option2','option3','option4','answer','section')


class StudentsDataAdmin(ImportExportModelAdmin):
    list_filter = ('roll_no', 'team_no', 'score')
    list_display = ('name', 'roll_no', 'score', 'team_no')


admin.site.register(students_data, StudentsDataAdmin)
