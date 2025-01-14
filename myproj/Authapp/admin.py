from django.contrib import admin

# Register your models here.
from Authapp.models import UserProfile, CustomUser, MediaItem
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomUser)
admin.site.register(MediaItem)

#super user acc name = Testing email = Test@gmail.com ps = Test_LO_REG@
