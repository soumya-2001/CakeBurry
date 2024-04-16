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
    
class Shape(models.Model):
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
    shape_object = models.ManyToManyField(Shape)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class CakeVariant(models.Model):
    
    WEIGHT_CHOICES = [
        (0.5, '0.5 kg'),
        (1, '1 kg'),
        (1.5, '1.5 kg'),
        (2, '2 kg'),
        (2.5,'2.5kg'),
        (3, '3 kg'),
        (4, '4 kg'),
        (5, '5 kg'),
        (200, '200 ml'),
        (375, '375 ml'),
        # Add more options as needed
    ]
    
    cake_object = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name="cakeproduct")
    weight_in_kg = models.DecimalField(max_digits=10, decimal_places=2, choices=WEIGHT_CHOICES, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    
class Basket(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    @property
    def cart_items(self):
        return self.cartitem.filter(is_order_placed=False)
    
    @property
    def cart_item_count(self):
        return self.cart_items.count()
    
    @property
    def basket_total(self):
        basket_items=self.cart_items
        if basket_items:
            total=sum([bi.item_total for bi in basket_items])
            return total
        return 0
    
class BasketItem(models.Model):
    cakevarient_object=models.ForeignKey(CakeVariant,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    occasion_object=models.ForeignKey(Occasion,on_delete=models.CASCADE,null=True)
    flavour_object=models.ForeignKey(Flavour,on_delete=models.CASCADE,null=True)
    shape_object=models.ForeignKey(Shape,on_delete=models.CASCADE,null=True)
    basket_object=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    note = models.TextField(blank=True) 
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_order_placed=models.BooleanField(default=False)
    
    @property
    def item_total(self):
        return self.qty*self.cakevarient_object.price
    

class Order(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    delivery_address=models.CharField(max_length=200)
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=200,null=True)
    is_paid=models.BooleanField(default=False)
    total=models.PositiveIntegerField()
    order_id=models.CharField(max_length=200,null=True)
    options=(
        ("cod","cod"),
        ("online","online")
    )
    payment=models.CharField(max_length=200,choices=options,default="cod")
    option=(
        ("order-placed","order-placed"),
        ("intransit","intransit"),
        ("dispatched","dispatched"),
        ("delivered","delivered"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=option,default="order-placed")
    
    @property
    def get_order_items(self):
        return self.purchaseitems.all()
    
    @property
    def get_order_total(self):
        purchase_items=self.get_order_items
        order_total=0
        if purchase_items:
            order_total=sum([pi.basket_item_object.item_total for pi in purchase_items])
            return order_total

class OrderItems(models.Model):
    order_object=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="purchaseitems")
    basket_item_object=models.ForeignKey(BasketItem,on_delete=models.CASCADE)
     

def create_basket(sender,instance,created,**kwargs):
    #created=T\F
    #sender=user
    #user=Sneha(who is registered)
    if created:    
        Basket.objects.create(owner=instance)
        
post_save.connect(create_basket,sender=User)
