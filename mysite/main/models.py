from django.db import models
from django.utils import timezone
# Create your models here.

class EssaySeries(models.Model):
	series_title = models.CharField(max_length=100)
	series_summary = models.CharField(max_length=200)
	series_slug = models.CharField(max_length=50, default=1)
	
	class Meta:
		verbose_name_plural = "Series"
	
	def __str__(self):
		return self.series_title
		
		
class Essay(models.Model):
	essay_title = models.CharField(max_length=100)
	essy_published = models.DateTimeField("Date Published", default=timezone.now)
	essay_content = models.TextField()

	
	series_title = models.ForeignKey(EssaySeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
	essay_slug = models.CharField(max_length=50, default=1)
	
	def __str__(self):
		return self.essay_title
	
	
