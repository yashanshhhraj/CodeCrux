# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Campaign, Reward, VendorWarning, WasteTracking

class CustomLoginForm(forms.Form):
    USER_TYPE_CHOICES = (
        ('', 'Select User Type'),
        ('public', 'Public User'),
        ('municipal', 'Municipal Corporation'),
        ('vendor', 'Vendor'),
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select()
    )

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        # Apply Tailwind classes dynamically to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            })

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        if not user_type:
            raise forms.ValidationError("Please select a user type")

        return cleaned_data

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('', 'Select User Type'),
        ('public', 'Public User'),
        ('municipal', 'Municipal Corporation'),
        ('vendor', 'Vendor'),
    ]

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput()
    )
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.Select())
    phone_number = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        # Common Tailwind CSS styles for input fields
        field_classes = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                # Apply Tailwind styles to dropdowns
                field.widget.attrs.update({'class': field_classes + " bg-white"})
            elif isinstance(field.widget, forms.PasswordInput):
                # Apply Tailwind styles to password fields
                field.widget.attrs.update({'class': field_classes, 'placeholder': f'Enter your {field_name.replace("_", " ")}'})
            else:
                # Apply Tailwind styles to text fields
                field.widget.attrs.update({'class': field_classes, 'placeholder': f'Enter your {field_name.replace("_", " ")}'})

    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        if not user_type:
            raise forms.ValidationError("Please select a user type")
        return user_type

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Update user profile after saving
            user.profile.user_type = self.cleaned_data['user_type']
            user.profile.phone_number = self.cleaned_data['phone_number']
            user.profile.save()

        return user


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'start_date', 'end_date', 'target_audience', 'budget']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'points_required', 'image', 'active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class WarningForm(forms.ModelForm):
    class Meta:
        model = VendorWarning
        fields = ['vendor', 'issue_type', 'description', 'level', 'action_required']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'action_required': forms.Textarea(attrs={'rows': 3}),
        }

class WasteTrackingForm(forms.ModelForm):
    class Meta:
        model = WasteTracking
        fields = ['waste_type', 'quantity', 'collection_date', 'disposal_date', 'disposal_method', 'disposal_proof', 'notes']
        widgets = {
            'collection_date': forms.DateInput(attrs={'type': 'date'}),
            'disposal_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }