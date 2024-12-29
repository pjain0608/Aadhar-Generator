from django.db import models

class Aadhar(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.BigIntegerField(unique=True)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    img = models.ImageField(upload_to='Images')
    gender = models.CharField(max_length=32)
    address = models.TextField()
    fathers_name = models.CharField(max_length=100)
    mothers_name = models.CharField(max_length=100)
    aadhar = models.BigIntegerField(unique=True)
    otp = models.IntegerField(null=True, blank=True)  # OTP field for temporary storage

    def __str__(self):
        return self.first_name