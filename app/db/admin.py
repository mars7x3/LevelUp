from django.contrib import admin

from db.models import ClientProfile, StaffProfile, MyUser

admin.site.register(MyUser)
admin.site.register(ClientProfile)
admin.site.register(StaffProfile)
