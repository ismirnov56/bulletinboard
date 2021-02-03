from django.contrib import admin

# Register your models here.
from src.moderation.models import Moderation

admin.site.register(Moderation)
