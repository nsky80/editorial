from django.db import models
from django.utils import timezone
# delete image too when object were deleted
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.


class EssayCategory(models.Model):
	category_title = models.CharField(max_length=100)
	category_summary = models.CharField(max_length=200)
	category_slug = models.CharField(max_length=50, default=1)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.category_title


class EssaySeries(models.Model):
	series_title = models.CharField(max_length=100)
	series_summary = models.CharField(max_length=200)
	series_slug = models.CharField(max_length=50, default=1)
	
	category_title = models.ForeignKey(EssayCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)

	class Meta:
		verbose_name_plural = "Series"
	
	def __str__(self):
		return self.series_title
		
		
class Essay(models.Model):
	essay_title = models.CharField(max_length=100)
	essay_published = models.DateTimeField("Date Published", default=timezone.now)
	essay_content = models.TextField()
	essay_image = models.ImageField(upload_to="images/essay/", default="images/sample-1.jpg", blank=True, null=True)

	
	series_title = models.ForeignKey(EssaySeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
	essay_slug = models.CharField(max_length=50, default=1)
	
	def __str__(self):
		return self.essay_title
	

# for deleting images too whenever a object has been deleted
@receiver(post_delete, sender=Essay)
def submission_delete(sender, instance, **kwargs):
	instance.essay_image.delete(False) 
  