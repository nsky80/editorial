from django.contrib import admin
from .models import Essay, EssaySeries, EssayCategory


# Register your models here.
admin.site.register(Essay)
admin.site.register(EssaySeries)
admin.site.register(EssayCategory)