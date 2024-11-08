import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=50, default="")


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    # gives current timestamp if nothing is defined
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     firstName = models.CharField(max_length=50, default="")
#     lastName = models.CharField(max_length=50, default="")
#     username = models.CharField(max_length=50, default="")
#     password = models.CharField(max_length=50)
#     email = models.CharField(max_length=50, default="")
#     phone = models.CharField(max_length=50, default="")
#     address = models.CharField(max_length=111)

#     def __str__(self):
#         return self.username

# class UserProfile(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     firstName = models.CharField(max_length=50, default="")
#     lastName = models.CharField(max_length=50, default="")
#     username = models.CharField(max_length=50, default="")
#     password = models.CharField(max_length=255)  # Increase the length for hashed password
#     email = models.CharField(max_length=50, default="")
#     phone = models.CharField(max_length=50, default="")
#     address = models.CharField(max_length=111)
#
#     def __str__(self):
#         return self.username
#
#     def set_password(self, raw_password):
#         """
#         Hash the password before saving it.
#         """
#         self.password = make_password(raw_password)
#
#     def check_password(self, raw_password):
#         """
#         Verify the password by comparing the raw password with the stored hash.
#         """
#         return check_password(raw_password, self.password)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=111, default="")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)

    def __str__(self):
        return str(self.username)



