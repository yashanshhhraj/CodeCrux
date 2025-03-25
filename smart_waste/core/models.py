from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('public', 'Public User'),
        ('municipal', 'Municipal Corporation'),
        ('vendor', 'Vendor'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='public')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile ({self.get_user_type_display()})"

# Create a UserProfile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Additional models for different user types
class MunicipalProfile(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='municipal_details')
    municipality_name = models.CharField(max_length=200)
    jurisdiction_area = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.municipality_name} ({self.profile.user.username})"

class VendorProfile(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='vendor_details')
    company_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    services_offered = models.TextField()
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.company_name} ({self.profile.user.username})"

class GarbageReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    GARBAGE_TYPE_CHOICES = (
        ('general', 'General Waste'),
        ('recyclable', 'Recyclables'),
        ('organic', 'Organic Waste'),
        ('hazardous', 'Hazardous Waste'),
        ('electronic', 'Electronic Waste'),
    )
    
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255)
    garbage_type = models.CharField(max_length=50, choices=GARBAGE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Report at {self.location} ({self.get_status_display()})"

class CollectionVehicle(models.Model):
    vehicle_id = models.CharField(max_length=50, unique=True)
    driver_name = models.CharField(max_length=100)
    current_location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Vehicle {self.vehicle_id} - {self.driver_name}"

class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.IntegerField()
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='reward_images/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Campaign(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    target_audience = models.CharField(max_length=100, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class WasteType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    recyclable = models.BooleanField(default=False)
    hazardous = models.BooleanField(default=False)
    points_value = models.IntegerField(default=1)
    
    def __str__(self):
        return self.name

class Zone(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    area_sqkm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    population = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    contract_start = models.DateField()
    contract_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def calculate_rating(self):
        """Calculate vendor rating based on various factors"""
        # This is a placeholder implementation
        warnings_count = self.warnings.count()
        if warnings_count == 0:
            return 5.0
            
        # Base rating of 5, deduct for warnings based on severity
        rating = 5.0
        
        critical = self.warnings.filter(level='critical').count() * 1.0
        high = self.warnings.filter(level='high').count() * 0.5
        medium = self.warnings.filter(level='medium').count() * 0.25
        low = self.warnings.filter(level='low').count() * 0.1
        
        deduction = critical + high + medium + low
        rating = max(1.0, rating - deduction)
        
        return round(rating, 1)

class Vehicle(models.Model):
    vehicle_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=50)
    capacity = models.DecimalField(max_digits=8, decimal_places=2)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=15, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, related_name='vehicles')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vehicles')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # These fields would typically be calculated from related models
    # but we include them here for simplicity
    collections = models.IntegerField(default=0)
    efficiency = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    def __str__(self):
        return f"{self.vehicle_id} - {self.driver_name}"

class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE, related_name='reports')
    image = models.ImageField(upload_to='report_images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    assigned_to = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_reports')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_reports')
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def mark_as_resolved(self, resolved_by=None):
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.save()
        
        # Award points to the user who reported this
        if self.reported_by and hasattr(self.reported_by, 'profile'):
            profile = self.reported_by.profile
            points_to_add = self.waste_type.points_value if self.waste_type else 1
            profile.points += points_to_add
            
            # Update level based on points (simple logic)
            if profile.points >= 100:
                profile.level = 3
            elif profile.points >= 50:
                profile.level = 2
            
            profile.save()

class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.IntegerField()
    image = models.ImageField(upload_to='reward_images/', null=True, blank=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class RewardClaim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reward_claims')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='claims')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    claimed_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_claims')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.reward.name} - {self.get_status_display()}"

class VendorWarning(models.Model):
    LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='warnings')
    issue_type = models.CharField(max_length=50)
    description = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='medium')
    action_required = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issued_warnings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.vendor.name} - {self.issue_type} - {self.get_status_display()}"