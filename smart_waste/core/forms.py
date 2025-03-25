# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Campaign, Reward, VendorWarning

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

class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('', 'Select User Type'),
        ('public', 'Public User'),
        ('municipal', 'Municipal Corporation'),
        ('vendor', 'Vendor'),
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Update widget attributes for built-in fields
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
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
            # Profile is created via signals, now we update it
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