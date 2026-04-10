from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
import os
import uuid
from taggit.managers import TaggableManager

User = get_user_model()

def image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('product_images', filename)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    tags = TaggableManager()
    count = models.IntegerField()
    description = models.TextField()
    attributes = models.JSONField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, default=None)

    def __str__(self):
        return f"{self.name} {self.price}"

class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=image_path)

class OrderLog(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    log = models.ForeignKey(OrderLog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    type_of_delivery = models.CharField(max_length=2, choices=[("NP", "Нова пошта"), ("UP", "Укр пошта")], default="NP")
    type_of_payment = models.CharField(max_length=2, choices=[("IP", "Оплата на місці")], default="IP")
    city = models.CharField(max_length=60)
    postoffice = models.CharField(max_length=60)
    ordered_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Замовлення {self.id}\nТовар: {self.log.product.name}\nЦіна: {self.log.product.price * self.log.count}₴\nЗамовник: {self.fullname}\nТелефон: {self.phone_number}\nДоставка: {self.get_type_of_delivery_display()}\nСпосіб оплати: {self.get_type_of_payment_display()}\nМісто: {self.city}\nПоштовий відділ: {self.postoffice}\nБуло замовлено: {self.ordered_at}"

class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField()

    @property
    def total_price(self):
        return self.product.price * self.count