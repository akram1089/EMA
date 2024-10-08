from django.db import models

# Address Details Model
class Address(models.Model):
    hno = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.hno}, {self.street}, {self.city}, {self.state}"

# Work Experience Model
class WorkExperience(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='work_experiences')
    companyName = models.CharField(max_length=255)
    fromDate = models.DateField()
    toDate = models.DateField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.companyName} ({self.fromDate} to {self.toDate})"

# Qualification Model
class Qualification(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='qualifications')
    qualificationName = models.CharField(max_length=255)
    percentage = models.FloatField()

    def __str__(self):
        return self.qualificationName

# Project Model
class Project(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='media/emp_photos/', blank=True, null=True)

    def __str__(self):
        return self.title

# Employee Model
class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phoneNo = models.CharField(max_length=15)

    # ForeignKey Relationship with Address
    addressDetails = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='employee_address')

    def __str__(self):
        return self.name
