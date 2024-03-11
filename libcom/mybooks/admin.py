from django.contrib import admin
from .models import Rating
from .models import User2Book
from .models import Status

admin.site.register(Rating)
admin.site.register(User2Book)
admin.site.register(Status)