from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.utils.translation import gettext_lazy as _



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'language', 
            'image', 
            'subscribe_to_food_blogs', 
            'subscribe_to_Life_in_Moscow_blogs', 
            'twitter_link', 
            'instagram_link', 
            'facebook_link'
            ]

    def clean_facebook_link(self, *args, **kwargs):
        facebook_link = self.cleaned_data.get("facebook_link")
        if facebook_link != '':
            if "https://" not in facebook_link:
                raise forms.ValidationError("Please include 'https://' in your link! (Ex: https://facebook.com/whattheblin)")
            if "facebook" not in facebook_link:
                raise forms.ValidationError("Facebook URLs only! (Ex: https://facebook.com/whattheblin)")
            if ".com" not in facebook_link:
                raise forms.ValidationError("Check spelling. (Ex: https://facebook.com/whattheblin)")
        return facebook_link

    def clean_instagram_link(self, *args, **kwargs):
        instagram_link = self.cleaned_data.get("instagram_link")
        if instagram_link != '':
            if "https://" not in instagram_link:
                raise forms.ValidationError("Please include 'https://' in your link! (Ex: https://instagram.com/whattheblin)")
            if "instagram" not in instagram_link:
                raise forms.ValidationError("Instagram URLs only! (Ex: https://instagram.com/whattheblin)")
            if ".com" not in instagram_link:
                raise forms.ValidationError("Check spelling. (Ex: https://instagram.com/whattheblin)")
        return instagram_link
    
    def clean_twitter_link(self, *args, **kwargs):
        twitter_link = self.cleaned_data.get("twitter_link")
        if twitter_link != '':
            if "https://" not in twitter_link:
                raise forms.ValidationError("Please include 'https://' in your link! (Ex: https://twitter.com/whattheblin)")
            if "twitter" not in twitter_link:
                raise forms.ValidationError("Twitter URLs only! (Ex: https://twitter.com/whattheblin)")
            if ".com" not in twitter_link:
                raise forms.ValidationError("Check spelling. (Ex: https://twitter.com/whattheblin)")
        return twitter_link
    