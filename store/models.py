import email
from email import message
from django.db import models
from distutils.command.upload import upload
from pyexpat import model
from statistics import mode
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    mobile =models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    area = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id)

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


CATEGORY_CHOICE = (
    ('CE', 'Covid Essential'),
    ('FC', 'Family Care'),
    ('PC', 'Personal Care'),
    ('A', 'Ayurvedic'),
    ('S', 'Surgical'),
    ('D', 'Devices'),
    ('IB', 'Immunity Booster'),
    ('M', 'Medicne'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=3, null='True')
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    product_image = models.ImageField(upload_to='store/static/online', null='True')

    def __str__(self):
        return str(self.id)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property 
    def total_cost(self):
        return self.quantity * self.product.selling_price

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Paid')
    payment_method = models.CharField(
        max_length=20, default="Cash On Delivery")
    payment_completed = models.BooleanField(
        default=True, null=True, blank=True)

    @property 
    def total_cost(self):
        return self.quantity * self.product.selling_price


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'message from ' + self.name + ' - ' + self.email

class Newsletter(models.Model):
    email = models.EmailField(max_length=50)

    def __str__(self):
        return 'Newsletter Sign Up from ' + self.email