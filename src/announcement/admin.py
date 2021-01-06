from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

admin.site.register(Categories, MPTTModelAdmin)
admin.site.register(Announcements)
admin.site.register(Images)