from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


GENDERS = (
    ("М", "Мужской"),
    ("Ж", "Женщина")
)

CONDITION = (
    ("Б", "Б/У"),
    ("Н", "Новое")
)

class Region(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class District(models.Model):
    title = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.title


class User(models.Model):
    photo = models.ImageField(upload_to='users/', blank=True, null=True, default="users/none_logo.png")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default='', blank=True)
    description = models.TextField(default='', blank=True)
    gender = models.CharField(max_length=255, choices=GENDERS, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True, related_name='district')
    phone_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\+375[0-9]{9}$',
                message="Введите номер в формате: '+375XXXXXXXXX'."
            )
        ],
        unique=True,
    )

    def __str__(self):
        return self.email

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='')
    cost = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(max_length=255, choices=CONDITION)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')

    def __str__(self):
        return f"Image for {self.product.title}"


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation between {', '.join([user.email for user in self.participants.all()])}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    text = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorites")

    def __str__(self):
        return f"{self.user.email} at {self.product.title}"

