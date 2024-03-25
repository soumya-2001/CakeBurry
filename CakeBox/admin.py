from django.contrib import admin
from CakeBox.models import Category,Occasion,Flavour,Cake,CakeVariant
# Register your models here.

admin.site.register(Category)
admin.site.register(Occasion)
admin.site.register(Flavour)
admin.site.register(Cake)
admin.site.register(CakeVariant)