import os
from django import forms
from .models import Ad, Job, AdEmail
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator, ValidationError


class AdForm(forms.ModelForm):

  class Meta:
    model = Ad
    
    fields = [
        'title',
        'main_image',
        'image_2',
        'image_3',
        'item_or_model_names',
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

  def clean(self):
  # "Cleaning and validating fields that depend on each other" - Django Docs
        cleaned_data = super().clean()
        main_image = cleaned_data.get("main_image")
        image_2 = cleaned_data.get("image_2")
        image_3 = cleaned_data.get("image_3")

        # Outcome #1: User only tries to upload image 3
        if 'default_ad' in image_2 and 'default_ad' in main_image:
            raise forms.ValidationError(
                  _("Upload Main Image and Image 2 before you try to upload Image 3.")
            )
        # Outcome #2: User only tries to upload image_2 and image_3
        if 'default_ad' in main_image:
            raise forms.ValidationError(
                _("Upload Main Image before you try to upload other images.")
            )
        # Outcome #3: User only tries to upload main_image and image_3
        if 'default_ad' in image_2:
            raise forms.ValidationError(
                _("Upload Image 2 before you try to upload Image 3.")
            )
                   

class JobForm(forms.ModelForm):
  class Meta:
    model = Job
    fields = [
        'title',
        'main_image',
        'image_2',
        'image_3',
        'title_of_position',
        'position_type',
        'experience',
        'degree_required',
        'salary',
        'location',
        'involves_travel',
        'company_name',
        'company_website',
        'skype_id',
        'job_description',
        ]

  def clean_recipients(self):
    company_website = self.cleaned_data['company_website']
    try:
      URLValidator(company_website)
    except:
      raise ValidationError("You have forgotten about Fred!")



class SendEmailForm(forms.ModelForm):
  class Meta: 
    model = AdEmail
    fields = [
      'title',
      'description',
    ]
