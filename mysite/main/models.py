from django.db import models
from django.utils import timezone
# delete image too when object were deleted
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
# Create your models here.


"""
Hierarchy used in DataBase
		EssayCategory
			|
		EssaySeries
			|
		Essay

Here Essay name is used only for illustration purpose i.e. makes things easier to understand
"""


# Highest in Hierarchy 
class EssayCategory(models.Model):
	category_title = models.CharField(max_length=100)
	category_summary = models.CharField(max_length=200)
	category_slug = models.CharField(max_length=50, default=1)
	category_image = models.ImageField(upload_to="images/category/", default="images/sample-1.jpg", blank=True, null=True)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.category_title


class EssaySeries(models.Model):
	series_title = models.CharField(max_length=100)
	series_summary = models.CharField(max_length=200)
	series_slug = models.CharField(max_length=50, default=1)
	series_image = models.ImageField(upload_to="images/series/", default="images/sample-1.jpg", blank=True, null=True)

	# series referencing category title of EssayCategory
	category_title = models.ForeignKey(EssayCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)

	class Meta:
		verbose_name_plural = "Series"
	
	def __str__(self):
		return self.series_title
		
		
class Essay(models.Model):

	# Here name `essay` is used only for illustration purpose i.e. easy to design

	essay_title = models.CharField("Content Title", max_length=100)
	essay_published = models.DateTimeField("Date Published", default=timezone.now)
	essay_content = models.TextField("Main Content", help_text='Write here your message!')

	# Only authenticated users can write new content so it refer to USER_MODEL and default is admin
	essay_contributor = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.SET_DEFAULT)
	
	series_title = models.ForeignKey(EssaySeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
	category_title = models.ForeignKey(EssayCategory, verbose_name="Category", default=1, on_delete=models.SET_DEFAULT)
	
	essay_slug = models.CharField(max_length=50, default=1)
	essay_image = models.ImageField("Display Image(Optional)", upload_to="images/essay/", default="images/sample-1.jpg", blank=True, null=True)
	
	# new field added
	essay_summary = models.CharField("Content Summary(About)", max_length=150, help_text="Write summary here!(Optional)", null=True, blank=True)

	def __str__(self):
		return self.essay_title
	

# for deleting images too whenever a object has been deleted
@receiver(post_delete, sender=Essay)
def submission_delete(sender, instance, **kwargs):
	instance.essay_image.delete(False) 
  

# Feedback Database, since it is open for all that's why doesn't used User as foreign key
class Feedback(models.Model):
	feedback_title = models.CharField(max_length=100)
	feedback_date = models.DateTimeField("Feedback Time", default=timezone.now)
	feedback_content = models.TextField(help_text="Share Your Ideas Here!")
	feedback_user_id = models.EmailField("Email ID")