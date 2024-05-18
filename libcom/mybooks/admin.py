from django.contrib import admin
from .models import Rating
from .models import User2Book
from .models import Status

class MyModelAdmin(admin.ModelAdmin):
    list_display = ['general', 'plot', 'characters', 'style', 'review', 'add_date']  # Поля, которые вы хотите отображать в списке
   # search_fields = ['field1', 'field2']  # Поля, по которым можно осуществлять поиск
   # readonly_fields = ('field3',)

admin.site.register(Rating, MyModelAdmin)
admin.site.register(User2Book)
admin.site.register(Status)