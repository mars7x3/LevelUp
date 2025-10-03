from django.contrib import admin

from db.models import *

admin.site.register(MyUser)
admin.site.register(ClientProfile)
admin.site.register(StaffProfile)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductCode)

