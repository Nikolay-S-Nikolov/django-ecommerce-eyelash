from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User_model = get_user_model()

class Product(models.Model):
    MAX_NAME_LENGTH = 30
    MAX_DESCRIPTION_LENGTH = 600
    
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        unique=True,
        )
    
    description = models.TextField(
        max_length=MAX_DESCRIPTION_LENGTH,
    )
    
    price = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        )

    stock = models.PositiveIntegerField()
    
    units_sold = models.PositiveIntegerField(
        default=0,
    )
    
    user = models.ForeignKey(
        User_model,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        )

    slug = models.SlugField(
        unique= True,
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
        )
    
    updated_at = models.DateTimeField(
        auto_now=True
        )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)  
        super().save(*args, **kwargs)
        
class ProductImages(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"