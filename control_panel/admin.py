from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(TransactionCredentials)
admin.site.register(PaymentMethod)
admin.site.register(GiftCard)

