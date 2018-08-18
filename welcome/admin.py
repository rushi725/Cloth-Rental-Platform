from django.contrib import admin
from .models import Product
from .models import Order
from .models import Image
from .models import Address, Category, CartP

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(CartP)
