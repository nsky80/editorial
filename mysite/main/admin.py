from django.contrib import admin
from .models import Essay, EssaySeries, EssayCategory, Feedback
from tinymce.widgets import TinyMCE
from django.db import models


class EssayCategoryAdmin(admin.ModelAdmin):
    list_display = ["category_title", "category_summary"]
    ordering = ["category_title"]
    fieldsets = [
        ("Basics", {"fields": ["category_title", "category_summary", "category_slug"]}),
        ("Media", {"fields": ["category_image"]}),
    ]

class EssayInline(admin.StackedInline):
    model = Essay
    extra = 2

class EssaySeriesAdmin(admin.ModelAdmin):
    list_filter = ['category_title']
    list_display = ('series_title', 'category_title')
    ordering = ['category_title']
    fieldsets = [
        (None,               {'fields': ['series_title', 'series_summary', 'series_slug']}),
        ('Contents', {'fields': ['series_image', 'category_title'], 'classes': ['collapse']}),
    ]
    inlines = [EssayInline]

class EssayAdmin(admin.ModelAdmin):
    list_display = ('essay_title', 'series_title', 'category_title', "essay_contributor", 'essay_published')   # displays the info in row
    list_filter = ['series_title', 'category_title', 'essay_published', "essay_contributor",]
    # search_fields = ['essay_title', 'series_title']
    ordering = ['series_title']

    fieldsets = [
        ("Title/date", {'fields': ["essay_title", "essay_published", "essay_contributor",]}),
        ("Series/Slug", {'fields': ['category_title', "series_title", "essay_slug"]}),
        ("Content", {"fields": ["essay_image", "essay_summary", "essay_content"]}),
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_title', 'feedback_user_id', 'feedback_date')   # displays the info in row
    list_filter = ['feedback_user_id', 'feedback_date']
    # search_fields = ['essay_title', 'series_title']
    ordering = ['feedback_date']

    fieldsets = [
        ("Title/date", {'fields': ["feedback_title", "feedback_date", "feedback_user_id",]}),
        ("Content", {'fields': ['feedback_content']}),
    ]

# Register your models here.
admin.site.register(Essay, EssayAdmin)    # this overrides default by above cofig
admin.site.register(EssaySeries, EssaySeriesAdmin)
admin.site.register(EssayCategory, EssayCategoryAdmin)
admin.site.register(Feedback, FeedbackAdmin)