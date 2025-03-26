# forms.py
from django import forms
from .models import Campaign, Reward, VendorWarning, WasteTracking
from werkzeug.security import generate_password_hash, check_password_hash
from django.conf import settings 

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
        """Authenticate the user manually with MongoDB"""
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user_type = cleaned_data.get("user_type")

        if not user_type:
            raise forms.ValidationError("Please select a user type")

        # Get MongoDB collection
        db = settings.MONGO_DB
        users_collection = db["users"]

        # Find user in MongoDB
        user = users_collection.find_one({"username": username})

        if not user:
            raise forms.ValidationError("Invalid username or password")

        if not check_password_hash(user["password"], password):  # Verify password
            raise forms.ValidationError("Invalid username or password")

        if user["user_type"] != user_type:  # Verify user type
            raise forms.ValidationError("Incorrect user type for this account")

        return cleaned_data

class UserRegistrationForm(forms.Form):
    USER_TYPE_CHOICES = [
        ('', 'Select User Type'),
        ('public', 'Public User'),
        ('municipal', 'Municipal Corporation'),
        ('vendor', 'Vendor'),
    ]

    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.Select())
    phone_number = forms.CharField(required=False, widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        # Common Tailwind CSS styles for input fields
        field_classes = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': field_classes + " bg-white"})
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({'class': field_classes, 'placeholder': f'Enter your {field_name.replace("_", " ")}'})
            else:
                field.widget.attrs.update({'class': field_classes, 'placeholder': f'Enter your {field_name.replace("_", " ")}'})

    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        if not user_type:
            raise forms.ValidationError("Please select a user type")
        return user_type

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match!")

        return cleaned_data

    def save(self):
        user_data = {
            "username": self.cleaned_data["username"],
            "email": self.cleaned_data["email"],
            "first_name": self.cleaned_data["first_name"],
            "last_name": self.cleaned_data["last_name"],
            "user_type": self.cleaned_data["user_type"],
            "phone_number": self.cleaned_data.get("phone_number", ""),
            "password": generate_password_hash(self.cleaned_data["password1"]),  # Use password1
        }
        settings.MONGO_COLLECTION.insert_one(user_data)  # Save to MongoDB
        return user_data


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