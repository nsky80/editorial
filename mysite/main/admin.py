from django.contrib import admin
from .models import Essay, EssaySeries, EssayCategory
from tinymce.widgets import TinyMCE
from django.db import models

class EssayAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title/date", {'fields': ["essay_title", "essay_published"]}),
        ("Series/Slug", {'fields': ["series_title", "essay_slug"]}),
        ("Content", {"fields": ["essay_image", "essay_content"]}),
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }

# Register your models here.
admin.site.register(Essay, EssayAdmin)    # this overrides default by above cofig
admin.site.register(EssaySeries)
admin.site.register(EssayCategory)