from django.contrib import admin

# Register your models here.
from core.models import *

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Style)
admin.site.register(Wishlist)
admin.site.register(Interest)
admin.site.register(Order)
admin.site.register(OrderProducts)
admin.site.register(ContactFormSubmissions)