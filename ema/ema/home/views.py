from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request,'home.html')
def all_emp(request):
    return render(request,'all_emp.html')
def profile_add(request):
    return render(request,'profile_add.html')

from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # Will raise error if validation fails
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):  # Will raise error if validation fails
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# import base64
# from django.core.files.base import ContentFile
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from .models import Profile
# from .serializers import ProfileSerializer

# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

#     def create(self, request, *args, **kwargs):
#         name = request.data.get('name')  # Get the name from the request
#         image_base64 = request.data.get('image')  # Get the Base64-encoded image string

#         # Ensure both name and image are provided
#         if not name or not image_base64:
#             return Response({"message": "Name and image are required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Decode the Base64 image
#         try:
#             format, imgstr = image_base64.split(';base64,')  # Split the format and image string
#             ext = format.split('/')[-1]  # Extract the image file extension (e.g., png, jpg)
#             image_data = ContentFile(base64.b64decode(imgstr), name=f"profile.{ext}")  # Decode and create ContentFile
#         except Exception as e:
#             return Response({"message": "Invalid image format."}, status=status.HTTP_400_BAD_REQUEST)

#         # Create the serializer with the decoded image and name
#         serializer = self.get_serializer(data={'name': name, 'image': image_data})

#         # Validate and save the data
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()  # Save the profile instance
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         # If data is invalid, return errors
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
