from django.contrib import admin
from .models import User, Messages, Topic, Room

# Register your models here.
admin.site.register(User)
admin.site.register(Messages)
admin.site.register(Room)
admin.site.register(Topic)
