from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Color(models.Model):
    colorList = [
        ('Сина', 'Blue'),
        ('Црвена', 'Red'),
        ('Зелена', 'Green'),
        ('Жолта', 'Yellow'),
        ('Розева', 'Pink'),
        ('Виолетова', 'Purple'),
        ('Црна', 'Black'),
        ('Бела', 'White')
    ]
    color=models.CharField(max_length=255,choices=colorList)

    def __str__(self):
        return self.color



class CustomUser(AbstractUser):
    image = models.ImageField(null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='custom_users', null=True, blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users', null=True, blank=True)

class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    conditionValues=[
        ('Лоша', 'Bad'),
        ('Средна', 'Average'),
        ('Добра', 'Good'),
        ('Одлична', 'Great')
    ]
    sizeValues=[
        ('XXS', 'Extra Extra Small'),
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large')
    ]
    condition = models.CharField(max_length=255,choices=conditionValues)
    size = models.CharField(max_length=255,choices=sizeValues)
    description = models.CharField(max_length=255)
    shop = models.CharField(max_length=255)
    typeClothes = [
        ('Фустан', 'Dress'),
        ('Панталони', 'Pants'),
        ('Блуза', 'Shirt'),
        ('Џемпер', 'Jumpers'),
        ('Јакна', 'Coat'),
        ('Фармерки', 'Jeans'),
        ('Аксесоари', 'Accessories'),
        ('Суќна', 'Skirt')
    ]
    type = models.CharField(max_length=255,choices=typeClothes)
    colors = models.ManyToManyField(Color, null=True, blank=True)
    genders=[
        ('M','Male'),
        ('F','Female')
    ]
    gender = models.CharField(max_length=255,choices=genders)
    sold = models.BooleanField(null=True,blank=True)
    sent = models.BooleanField(null=True,blank=True)
    date_sent=models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(null=True,blank=True)
    date_accepted = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.size+' '+self.shop+' '+self.type)

class ImageProd(models.Model):
    image=models.ImageField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')


class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_order=models.DateTimeField(auto_now=True)


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Delivery(models.Model):
    cart=models.ForeignKey(ShoppingCart,on_delete=models.CASCADE)
    phone=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    postal=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    finished=models.BooleanField(default=False)

class ShoppingItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.CharField(max_length=500)
    date = models.DateTimeField()
    userFrom = models.ForeignKey(CustomUser, related_name='sent_comments',on_delete=models.CASCADE)
    userTo = models.ForeignKey(CustomUser, related_name='received_comments', on_delete=models.CASCADE)


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)