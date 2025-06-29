from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from django.utils import timezone


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/products/')

    def __str__(self):
        return f"{self.name}"

    def average_rating(self):
        rating = Review.objects.filter(product=self).aggregate(Avg('grade'))
        print(f'rating={rating} product={self.name}')
        return int(rating['grade__avg']) if rating['grade__avg'] is not None else None


class Review(models.Model):
    text = models.TextField()
    grade = models.PositiveIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product} {self.grade}"