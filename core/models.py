from django.db import models
from django.contrib.auth.models import User
import datetime
# Town model to store town names and their price
class Town(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class student(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    course=models.CharField(max_length=100)
    academic_year=models.CharField(max_length=30)
    photo=models.ImageField(upload_to="student_photos/")
    town=models.ForeignKey(Town,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.full_name
class Clerk(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class buspass(models.Model):
    student=models.ForeignKey(student,on_delete=models.CASCADE)
    month=models.CharField(max_length=15)
    year=models.IntegerField(default=datetime.datetime.now().year)
    is_renewed=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student.full_name}"
    class Meta:
     unique_together = ('student', 'month', 'year')
    

