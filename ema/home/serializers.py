from rest_framework import serializers
from .models import Employee, WorkExperience, Qualification, Project, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['hno', 'street', 'city', 'state']
        extra_kwargs = {
            'hno': {'required': False},
            'street': {'required': False},
            'city': {'required': False},
            'state': {'required': False},
        }

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['companyName', 'fromDate', 'toDate', 'address']
        extra_kwargs = {
            'companyName': {'required': False},
            'fromDate': {'required': False},
            'toDate': {'required': False},
            'address': {'required': False},
        }

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['qualificationName', 'percentage']
        extra_kwargs = {
            'qualificationName': {'required': False},
            'percentage': {'required': False},
        }

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'photo']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'photo': {'required': False},
        }

class EmployeeSerializer(serializers.ModelSerializer):
    addressDetails = AddressSerializer(required=False)  # Make nested address data optional
    work_experiences = WorkExperienceSerializer(many=True, required=False)  # Make work experiences optional
    qualifications = QualificationSerializer(many=True, required=False)  # Make qualifications optional
    projects = ProjectSerializer(many=True, required=False)  # Make projects optional

    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'email', 'age', 'gender', 'phoneNo',
            'addressDetails', 'work_experiences', 'qualifications', 'projects'
        ]

    def create(self, validated_data):
        print("validated_data", validated_data)
        address_data = validated_data.pop('addressDetails')  # Pop the address details
        work_experience_data = validated_data.pop('work_experiences', [])
        qualification_data = validated_data.pop('qualifications', [])
        project_data = validated_data.pop('projects', [])

        # Create the address instance
        address = Address.objects.create(**address_data)

        # Create the employee instance with the address
        employee = Employee.objects.create(addressDetails=address, **validated_data)

        # Create work experiences
        for work in work_experience_data:
            WorkExperience.objects.create(employee=employee, **work)

        # Create qualifications
        for qualification in qualification_data:
            Qualification.objects.create(employee=employee, **qualification)

        # Create projects
        for project in project_data:
            Project.objects.create(employee=employee, **project)

        return employee
