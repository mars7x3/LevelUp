from django.contrib import admin
from nested_admin.nested import NestedStackedInline, NestedModelAdmin

from db.models import *

admin.site.register(MyUser)
admin.site.register(ClientProfile)
admin.site.register(StaffProfile)
admin.site.register(Order)
admin.site.register(Work)
admin.site.register(WorkImage)
admin.site.register(Statement)

class ProductCodeInline(NestedStackedInline):
    model = ProductCode
    extra = 0


@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    inlines = (ProductCodeInline, )