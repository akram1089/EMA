
from django.contrib import admin
from .models import Employee, Address, WorkExperience, Qualification, Project

admin.site.register(Employee)
admin.site.register(Address)
admin.site.register(WorkExperience)
admin.site.register(Qualification)
admin.site.register(Project)
