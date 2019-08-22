from django import forms 
from .models import EssaySeries, Essay, Feedback
# from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


# TinyMCE editer for writing new content used both end User and Admin
class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


# This is form for writing new content by user
class Write_content(forms.ModelForm):
    # essay_published = forms.DateTimeField(widget=forms.SplitDateTimeWidget)
    essay_content = forms.CharField(label="Main Content", 
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = Essay
        fields = ['essay_title', 'essay_published', 'series_title', 'essay_image', 'essay_summary', 'essay_content',] # or whatever fields you want ('field_a', )


# User can modify his information and it allows only what user can modify
class EditProfileForm(UserChangeForm):
     class Meta:
         model = User
         fields = (
             'username',
             'email',
             'first_name',
             'last_name',
         )
        #  exclude = ()


# This is feedback form which is open to all but id required
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('feedback_title', 'feedback_user_id', 'feedback_content')


# This class is added only for testing purposes it will remove soon!
class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(       # A hidden input for internal use
        max_length=50,              # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')
