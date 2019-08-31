from django import forms
from .models import Ad, Job, AdEmail

class AdForm(forms.ModelForm):
  class Meta:
    model = Ad
    fields = [
        'title',
        'image_1',
        'image_2',
        'image_3',
        'items_or_model_names',
        'category',
        'buying_or_selling',
        'condition',
        'asking_price',
        'location',
        'willing_to_travel',
        'twitter_contact',
        'instagram_contact',
        'facebook_contact',
        'description',
        ]


class JobForm(forms.ModelForm):
  class Meta:
    model = Job
    fields = [
        'title',
        'image',
        'title_of_position',
        'position_type',
        'experience',
        'education',
        'salary',
        'location',
        'involves_travel',
        'name',
        'company_description',
        'company_website',
        'email',
        'skype_id',
        'job_description',
        ]



class SendEmailForm(forms.ModelForm):
  class Meta: 
    model = AdEmail
    fields = [
      'title',
      'description',
    ]