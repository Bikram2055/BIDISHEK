from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Product(models.Model):
    image = models.ImageField(upload_to='products/', blank=True)
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    subtotal = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}/name:{self.item}/quantity:{self.quantity}/purchased:{self.purchased}'

    def get_total(self):
        total = self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}/order status:{self.ordered}'

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()

        return total


class shipment(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        contact = models.IntegerField()
        address = models.CharField(max_length=100)
        city = models.CharField(max_length=30)
        landmark = models.CharField(max_length=20)
        order = models.ForeignKey(Order, on_delete=models.CASCADE)

        def __str__(self):
            return f'{self.user.username}/{self.contact}/{self.address}/{self.city}/landmark:{self.landmark}'
