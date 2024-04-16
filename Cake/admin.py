from django.contrib import admin
from Cake.models import Category,Occasion,Flavour,Shape,Cake,CakeVariant
# Register your models here.

admin.site.register(Category)
admin.site.register(Occasion)
admin.site.register(Flavour)
admin.site.register(Shape)
admin.site.register(Cake)
admin.site.register(CakeVariant)
