from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Occasion(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Flavour(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Cake(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="cake_product_images", default="default.jpg", null=True, blank=True)
    category_object = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="cakecategory")
    occasion_object = models.ManyToManyField(Occasion)
    flavour_object = models.ManyToManyField(Flavour)
    # base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class CakeVariant(models.Model):
    SHAPE_CHOICES = [
        ('Round', 'Round'),
        ('Square', 'Square'),
        ('Heart', 'Heart'),
        ('Custom', 'Custom'),
        # Add more options as needed
    ]
    WEIGHT_CHOICES = [
        (0.5, '0.5 kg'),
        (1, '1 kg'),
        (1.5, '1.5 kg'),
        (3, '3 kg'),
        (4, '4 kg'),
        (5, '5 kg'),
        # Add more options as needed
    ]
    
    cake_object = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name="cakeproduct")
    shape = models.CharField(max_length=10, choices=SHAPE_CHOICES, default='Round') 
    weight_in_kg = models.DecimalField(max_digits=10, decimal_places=2, choices=WEIGHT_CHOICES, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    
class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
class BasketItem(models.Model):
    cakevarient_object=models.ForeignKey(CakeVariant,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    occasion_object=models.ForeignKey(Occasion,on_delete=models.CASCADE,null=True)
    flavour_object=models.ForeignKey(Flavour,on_delete=models.CASCADE,null=True)
    

def create_basket(sender,instance,created,**kwargs):
    #created=T\F
    #sender=user
    #user=Sneha(who is registered)
    if created:    
        Basket.objects.create(owner=instance)
        
post_save.connect(create_basket,sender=User)
    