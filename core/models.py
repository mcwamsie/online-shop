from django.db import models

from user_auth.models import User


# from django.contrib.auth.models import User


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500)
    status = models.BooleanField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Style(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500)
    status = models.BooleanField(default=1)
    choices = [
        ("MEN", "MEN"),
        ("CHILDREN", "CHILDREN"),
        ("BOYS", "BOYS"),
        ("GIRLS", "GIRLS"),
        ("WOMEN", "WOMEN"),
        ("UNISEX", "UNISEX")
    ]
    gender = models.CharField(choices=choices, max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=500)
    logo = models.ImageField(upload_to="brands")
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    style = models.ForeignKey(Style, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    quantity = models.IntegerField(default=0)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand.name + " - " + self.name


class Interest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #    unique_together = ["product", "user"]

    def __str__(self):
        return self.user.username + " - (" + str(self.product) + ")"


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["product", "user"]


class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)
    value = models.CharField(max_length=200)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rating = models.DecimalField(default=0, max_digits=1, decimal_places=0)


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=255)
    streetAddress = models.CharField(max_length=200, verbose_name="Street Address")
    town_or_city = models.CharField(max_length=200, verbose_name="Town/City")
    shipping_address = models.CharField(max_length=255, verbose_name="Shipping Address")
    shipping_town_or_city = models.CharField(max_length=200, verbose_name="Shipping Town/City")
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(default=0, max_digits=11, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    total_price = models.DecimalField(max_digits=11, decimal_places=2)


class ContactFormSubmissions(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    emailAddress = models.EmailField(max_length=255, verbose_name="Email Address")
    subject = models.CharField(max_length=255, verbose_name="Subject")
    message = models.TextField(max_length=1000, verbose_name="Message")
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.createdAt) + ":" + self.name + " - " + self.subject

    class Meta:
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"
