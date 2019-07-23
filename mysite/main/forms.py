from django import forms 
from .models import EssaySeries, Essay
# from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
# from django.contrib.flatpages.models import FlatPage


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False



class Write_content(forms.ModelForm):
    # essay_published = forms.DateTimeField(widget=forms.SplitDateTimeWidget)
    essay_content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    # class Meta:
    #     model = Post
    #     fields = '__all__'


    class Meta:
        model = Essay
        fields = ['essay_title', 'essay_published', 'series_title', 'essay_image', 'essay_content',] # or whatever fields you want ('field_a', )



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
