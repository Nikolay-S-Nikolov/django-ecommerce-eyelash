from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from lash_store.product.models import Product

UserModel = get_user_model()

class Order(models.Model):
    PRICE_MAX_DIGITS = 6
    PRICE_DECIMAL_PLACES = 2
    MAX_STATUS_LENGTH = 10
    STATUS_CHOICES = [
        ('Pending', 'Очаква се'),
        ('Processing', 'В обработка'),
        ('Completed', 'Завършена'),
        ('Cancelled', 'Отменена'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Неплатена'),
        ('paid', 'Платена'),
        ('refunded', 'Възстановена'),
    ]

    customer = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name='Клиент',
    )
    status = models.CharField(
        max_length=MAX_STATUS_LENGTH,
        choices=STATUS_CHOICES,
        default='Pending',
        verbose_name='Статус на поръчката',
    )

    total_price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        verbose_name='Обща сума',
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid',
        verbose_name='Статус на плащане',
    )

    note = models.TextField(
        blank=True,
        null=True,
        verbose_name='Бележка',
    )

    email_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата на създаване',
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Последна промяна',
    )

    def __str__(self):
        return f"Поръчка #{self.id} - статус: {self.get_status_display()}"

    @property
    def calculated_total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def clean(self):
        shipping = getattr(self, 'shippingaddress', None)
        if shipping and shipping.payment_method == 'bank_payment':
            if self.status in ['Processing', 'Completed'] and self.payment_status != 'paid':
                raise ValidationError("Поръчките с банково плащане трябва да бъдат платени преди да се обработят.")


class OrderItem(models.Model):
    PRICE_MAX_DIGITS = 6
    PRICE_DECIMAL_PLACES = 2

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name= 'Продукт'
    )

    quantity = models.PositiveIntegerField(
        verbose_name= 'Количество'
    )

    saved_price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        verbose_name= 'Стойност'
    )

    @property
    def price(self):
        return self.quantity * self.product.price

    def save(self, *args, **kwargs):
        # price calculation
        self.saved_price = self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Поръчани {self.quantity} бр. от {self.product}"


class Cart(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    def __str__(self):
        return f"{self.quantity} x {self.product} in cart"


class ShippingAddress(models.Model):
    MAX_CITY_LENGTH = 50
    MAX_NAME_LENGTH = 35
    MAX_PHONE_NUMBER_LENGTH = 13
    MAX_POSTAL_CODE_LENGTH = 4
    MAX_PAYMENT_METHOD_LENGTH = 20
    PAYMENT_CHOICES = [
        ('pay_on_delivery', 'Плати при доставка'),
        ('bank_payment', 'Банков превод'),
    ]

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name= 'Име за доставката'
    )

    phone_number = models.CharField(
        max_length=MAX_PHONE_NUMBER_LENGTH,
        validators=[RegexValidator(
            regex=r"^((?:\+359|0)8[7-9]\d{7}|(?:\+359|0)[2-9]\d{6,8})$",
            message="Моля въведете валиден телефоне номер с формат 0888123456"
        )],
        verbose_name='Телефонен номер за доставката'
    )

    email = models.EmailField()

    customer = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    address = models.TextField(
        verbose_name='Адрес за доставка'
    )

    city = models.CharField(
        max_length=MAX_CITY_LENGTH,
        verbose_name='Град'
    )

    postal_code = models.CharField(
        max_length=MAX_POSTAL_CODE_LENGTH,
        verbose_name='Пощенски код'
    )

    payment_method = models.CharField(
        max_length=MAX_PAYMENT_METHOD_LENGTH,
        choices=PAYMENT_CHOICES,
        default='pay_on_delivery',
        verbose_name='Мотод на плащане'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Адрес за доставка за {self.order}"