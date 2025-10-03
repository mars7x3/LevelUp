import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from db.enums import StaffRole, UserStatus, ProductStatus, CodeType, OrderStatus


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class MyUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    status = models.IntegerField(
        choices=UserStatus.choices,
        blank=True,
        null=True
    )


class StaffProfile(BaseModel):
    user = models.OneToOneField(
        'MyUser',
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    fullname = models.CharField(max_length=100)
    role = models.IntegerField(choices=StaffRole.choices)


class ClientProfile(BaseModel):
    user = models.OneToOneField(
        'MyUser',
        on_delete=models.CASCADE,
        related_name='client_profile'
    )
    fullname = models.CharField(max_length=100)


class Order(BaseModel):
    client = models.ForeignKey(
        'ClientProfile',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        blank=True,
        null=True
    )


class OrderProduct(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='order_products'
    )
    product_title = models.CharField(max_length=100)


class ProductDetail(BaseModel):
    order_product = models.ForeignKey(
        'OrderProduct',
        on_delete=models.CASCADE,
        related_name='details'
    )
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()


class Product(BaseModel):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='products'
    )
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    internal_code = models.CharField(max_length=200)
    status = models.IntegerField(
        choices=ProductStatus.choices,
        blank=True,
        null=True
    )


class ProductCode(BaseModel):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='codes'
    )
    file = models.FileField(upload_to='codes')
    code = models.CharField(max_length=200)
    type = models.IntegerField(
        choices=CodeType.choices,
        blank=True,
        null=True
    )


class Work(BaseModel):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='works'
    )
    staff = models.ForeignKey(
        'StaffProfile',
        on_delete=models.CASCADE,
        related_name='works'
    )
    comment = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    status = models.IntegerField(choices=ProductStatus.choices)


class WorkImage(BaseModel):
    work = models.ForeignKey(
        'Work',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='defects')
