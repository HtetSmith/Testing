from django.contrib import admin

# Register your models here.
from Authapp.models import UserProfile, CustomUser
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomUser)

#super user acc name = Testing email = Test@gmail.com ps = Test_LO_REG@
