from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):

    title = models.CharField(
        max_length=120
    )

    def __str__(self):
        return self.title


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category'
    )
    
    title = models.CharField(
        max_length=120,
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    price = models.PositiveIntegerField(
        default=0,
    )

    image = models.ImageField()

    def __str__(self):
        return self.title


class CartProduct(models.Model):

    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )


class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    products = models.ManyToManyField(
        Product,
        through=CartProduct,
        related_name='products',
    )

    total_price = models.IntegerField(
        default=0,
    )


class Order(models.Model):

    PAYMENT, DELIVERY, COMPLETED = range(3)

    ORDER_STATUSES = (
        (PAYMENT, 'PAYMENT'),
        (DELIVERY, 'DELIVERY'),
        (COMPLETED, 'COMPLETED'),
    )

    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    address = models.CharField(
        max_length=255,
    )

    status = models.IntegerField(
        choices=ORDER_STATUSES,
        default=PAYMENT,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def get_status(self):
        return self.ORDER_STATUSES[self.status][1]
