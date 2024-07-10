from django.db import models
from django.contrib.auth.models import AbstractUser
from random import sample
import string
from datetime import datetime


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 
    
    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/',default='avatar/default.png')
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.username}'
    
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'default.png'
        super().save(*args, **kwargs)
    

class Category(CodeGenerate):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Product(CodeGenerate):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, 
                                         blank=True, null=True)
    banner_img = models.ImageField(upload_to='banner-img/')
    quantity = models.IntegerField() 
    delivery = models.BooleanField(default=False)

    @property
    def stock_status(self):
        return bool(self.quantity)

    def __str__(self):
        return f'{self.name}'


class ProductImg(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img/')

    def __str__(self):
        return f'{self.product.name}'


class Cart(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    order_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(
        choices=(
            (1,'Nofaol'),
            (2,'Yo`lda'),
            (3,'Qaytarilgan'),
            (4,'Qabul qilingan')
        ))

    def __str__(self):
        return f'{self.user.username},{self.status}'
    
    def save(self, *args, **kwargs):
        if self.status == 2 and Cart.objects.get(id=self.id).status == 1:
            self.order_date = datetime.now()
        super(Cart,self).save(*args, **kwargs)

    @property
    def total(self):
        count = 0
        queryset = CartProduct.objects.filter(cart = self)
        for i in queryset:
            count +=i.count
        return count
    
    @property
    def price(self):
        count = 0
        queryset = CartProduct.objects.filter(cart = self)
        for i in queryset:
            if i.product.discount_price:
                count += i.count * i.product.discount_price
            else:
                count += i.count * i.product.price
        return count
    
    @property
    def total_price(self):
        count = 0
        queryset = CartProduct.objects.filter(cart = self)
        for i in queryset:
            count += i.count * i.product.price
        return count



class CartProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f'{self.product.name,self.count,self.cart.status}'

    @property
    def date(self):
        return self.cart.order_date
    
    @property
    def price(self):
        count = self.count * self.product.price
        return count
    
