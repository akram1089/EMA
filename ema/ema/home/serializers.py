from rest_framework import serializers
from .models import Employee, WorkExperience, Qualification, Project, Address
import base64
from django.core.files.base import ContentFile

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
from rest_framework import serializers
from .models import Project
import base64
from django.core.files.base import ContentFile

class ProjectSerializer(serializers.ModelSerializer):
    # Override the photo field to handle Base64 encoded images
    photo = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'photo']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'photo': {'required': False},
        }

    def validate(self, attrs):
        """Override validate to handle Base64 image decoding."""
        if 'photo' in attrs and attrs['photo']:
            title = attrs.get('title', 'project_image')  # Get the title or default to a placeholder
            try:
                format, imgstr = attrs['photo'].split(';base64,')  # Split the base64 string
                ext = format.split('/')[-1]  # Extract the file extension
                decoded_image = base64.b64decode(imgstr)

                # Use the title as the filename, sanitize it to avoid invalid characters
                sanitized_title = ''.join(e if e.isalnum() else '_' for e in title)
                attrs['photo'] = ContentFile(decoded_image, name=f"{sanitized_title}.{ext}")  # Update the attrs
            except Exception:
                raise serializers.ValidationError("Invalid image format")
        
        return super().validate(attrs)  # Call the parent class's validate method

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
        # Handle nested data like addressDetails, work_experiences, qualifications, and projects
        address_data = validated_data.pop('addressDetails', None)
        work_experience_data = validated_data.pop('work_experiences', [])
        qualification_data = validated_data.pop('qualifications', [])
        project_data = validated_data.pop('projects', [])

        # Create the address instance if provided
        address = Address.objects.create(**address_data) if address_data else None

        # Create the employee instance with the address
        employee = Employee.objects.create(addressDetails=address, **validated_data)

        # Create work experiences
        for work in work_experience_data:
            WorkExperience.objects.create(employee=employee, **work)

        # Create qualifications
        for qualification in qualification_data:
            Qualification.objects.create(employee=employee, **qualification)

        # Create projects with decoded Base64 images
        for project in project_data:
            Project.objects.create(employee=employee, **project)

        return employee



# from rest_framework import serializers
# from .models import Profile

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['id', 'name', 'image']
