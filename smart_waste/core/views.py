from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .forms import CustomLoginForm, UserRegistrationForm

def landing_page(request):
    features = [
        {
            "icon": '<svg class="h-10 w-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>',
            "title": "AI-Powered Detection",
            "description": "Advanced computer vision algorithms detect waste and monitor fill levels in real-time."
        },
        {
            "icon": '<svg class="h-10 w-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
            "title": "Smart Location Mapping",
            "description": "GPS tracking and mapping to optimize collection routes and identify waste hotspots."
        },
        {
            "icon": '<svg class="h-10 w-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
            "title": "Issue Reporting System",
            "description": "Citizen engagement platform for reporting waste issues and tracking resolution."
        },
        {
            "icon": '<svg class="h-10 w-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/></svg>',
            "title": "Analytics Dashboard",
            "description": "Comprehensive data analytics for waste trends, collection efficiency, and resource allocation."
        },
        {
            "icon": '<svg class="h-10 w-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>',
            "title": "Recycling Optimization",
            "description": "Smart sorting and recycling recommendations to maximize material recovery."
        },
        {
            "icon": '<svg class="h-10 w-10" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 22s4-2 8-2 8 2 8 2"/><line x1="2" y1="11" x2="22" y2="11"/><path d="M14 7.5a4 4 0 0 0-8 0H2v3h4a4 4 0 0 0 8 0h4v-3h-4Z"/></svg>',
            "title": "Environmental Impact",
            "description": "Measure and track sustainability metrics and carbon footprint reduction."
        }
    ]

    return render(request, 'core/landing.html', {'features': features})

def about_view(request):
    team_members = [
        {
            "name": "Himanshu Dhepe",
            "role": "Team Member",
            "bio": "Developer",
            "image": static('images/team/david-park.jpg'),
            "linkedin": "https://linkedin.com/in/example",
            "twitter": None
        },
        {
            "name": "Gajendra Singh",
            "role": "Team Member",
            "bio": "Full Stack Developer",
            "image": static('images/team/michael-rodriguez.jpg'),
            "linkedin": "https://linkedin.com/in/example",
            "twitter": None
        },
        {
            "name": "Pawan Kumar Rajak",
            "role": "Team Member",
            "bio": "Full Stack Developer",
            "image": static('images/team/aisha-nkosi.jpg'),
            "linkedin": "https://linkedin.com/in/example",
            "twitter": "https://twitter.com/example"
        },
        {
            "name": "Yashansh Raj Pandey",
            "role": "Team Leader",
            "bio": "Full Stack Developer",
            "image": static('images/team/sarah-chen.jpg'),
            "linkedin": "https://linkedin.com/in/example",
            "twitter": "https://twitter.com/example"
        },
    ]
    
    return render(request, 'core/about.html', {'team_members': team_members})

class LoginView(View):
    template_name = 'core/login.html'
    
    def get(self, request):
        # If user is already logged in, redirect to home
        if request.user.is_authenticated:
            return redirect('home')
        
        form = CustomLoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomLoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_type = form.cleaned_data.get('user_type')
            
            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Check if user type matches
                if hasattr(user, 'profile') and user.profile.user_type == user_type:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    
                    # Redirect based on user type
                    if user_type == 'public':
                        return redirect('public_dashboard')
                    elif user_type == 'municipal':
                        return redirect('municipal_dashboard')
                    elif user_type == 'vendor':
                        return redirect('vendor_dashboard')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, 'Invalid user type for this account.')
            else:
                messages.error(request, 'Invalid username or password.')
        
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out successfully.')
        return redirect('login')

class ForgotPasswordView(View):
    template_name = 'core/forgot_password.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        # Password reset logic would go here
        email = request.POST.get('email')
        # Send password reset email logic
        messages.info(request, f'Password reset instructions sent to {email}')
        return redirect('login')

class RegisterView(View):
    template_name = 'core/register.html'
    
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            # Create user profile with selected user type
            user_type = form.cleaned_data.get('user_type')
            user.profile.user_type = user_type
            user.profile.save()
            
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
        
        return render(request, self.template_name, {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GarbageReport, UserProfile, CollectionVehicle

def PublicDashboardView(request):
    """
    View for the public dashboard of CleanCity app.
    Shows garbage reports, collection vehicles, and waste management tips.
    """
    # Get recent reports to display in the table
    recent_reports = GarbageReport.objects.all().order_by('-created_at')[:10]
    
    # Get collection vehicles for the map
    collection_vehicles = CollectionVehicle.objects.filter(active=True)
    
    # Get collection points for the map
    collection_points = GarbageReport.objects.filter(status='pending')
    
    context = {
        'recent_reports': recent_reports,
        'collection_vehicles': collection_vehicles,
        'collection_points': collection_points,
    }
    
    return render(request, 'publicview.html', context)

@login_required
def user_dashboard(request):
    """
    View for the user's personal dashboard.
    Requires authentication and shows user-specific data.
    """
    # Get the user's profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get reports made by the user
    user_reports = GarbageReport.objects.filter(reporter=request.user).order_by('-created_at')
    
    context = {
        'user_profile': user_profile,
        'user_reports': user_reports,
    }
    
    return render(request, 'user_dashboard.html', context)

def report_garbage(request):
    """
    View for reporting garbage.
    Handles both GET (form display) and POST (form submission).
    """
    if request.method == 'POST':
        # Process the form submission
        location = request.POST.get('location')
        garbage_type = request.POST.get('garbage_type')
        description = request.POST.get('description')
        
        # Create a new garbage report
        report = GarbageReport.objects.create(
            reporter=request.user if request.user.is_authenticated else None,
            location=location,
            garbage_type=garbage_type,
            description=description,
            status='pending'
        )
        
        # Add points to user if authenticated
        if request.user.is_authenticated:
            profile = UserProfile.objects.get(user=request.user)
            profile.points += 10  # Award 10 points for reporting garbage
            profile.total_reports += 1
            profile.save()
            
        return redirect('report_success')
    
    # If GET request, just show the form
    return render(request, 'report_garbage.html')

def track_vehicle(request):
    """
    View for tracking garbage collection vehicles.
    """
    vehicles = CollectionVehicle.objects.filter(active=True)
    
    context = {
        'vehicles': vehicles,
    }
    
    return render(request, 'track_vehicle.html', context)

def rewards_dashboard(request):
    """
    View for the rewards page.
    """
    available_rewards = Reward.objects.filter(active=True)
    
    context = {
        'available_rewards': available_rewards,
    }
    
    return render(request, 'rewards_dashboard.html', context)

def all_reports(request):
    """
    View for displaying all garbage reports.
    """
    reports = GarbageReport.objects.all().order_by('-created_at')
    
    context = {
        'reports': reports,
    }
    
    return render(request, 'all_reports.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Avg, Sum, F, Q
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import csv
import io

from .models import (
    Campaign, 
    Reward, 
    UserProfile, 
    RewardClaim, 
    Report, 
    WasteType, 
    Zone, 
    Vehicle, 
    Vendor, 
    VendorWarning
)
from .forms import CampaignForm, RewardForm, WarningForm

def is_municipal_admin(user):
    return user.is_authenticated and user.is_staff and hasattr(user, 'profile') and user.profile.role == 'municipal_admin'

@login_required
@user_passes_test(is_municipal_admin)
def municipal_dashboard(request):
    # Get stats for the dashboard
    stats = {
        'total_reports': Report.objects.count(),
        'resolved_reports': Report.objects.filter(status='resolved').count(),
        'active_vehicles': Vehicle.objects.filter(active=True).count(),
        'pending_warnings': VendorWarning.objects.filter(status='pending').count(),
    }
    
    # Get campaigns with status color
    campaigns = Campaign.objects.all().order_by('-start_date')
    for campaign in campaigns:
        today = timezone.now().date()
        if campaign.start_date > today:
            campaign.status = 'pending'
            campaign.status_color = 'warning'
        elif campaign.end_date < today:
            campaign.status = 'completed'
            campaign.status_color = 'secondary'
        else:
            campaign.status = 'active'
            campaign.status_color = 'success'
    
    # Get rewards
    rewards = Reward.objects.all().order_by('-points_required')
    
    # Get top users
    top_users = UserProfile.objects.exclude(user__is_staff=True).order_by('-points')[:10]
    
    # Get recent reward claims
    recent_claims = RewardClaim.objects.all().order_by('-claimed_at')[:15]
    for claim in recent_claims:
        if claim.status == 'approved':
            claim.status_color = 'success'
        elif claim.status == 'pending':
            claim.status_color = 'warning'
        elif claim.status == 'rejected':
            claim.status_color = 'danger'
    
    # Chart data - get reports by month for the last 6 months
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=180)  # approximately 6 months
    
    report_data = (
        Report.objects
        .filter(created_at__gte=start_date, created_at__lte=end_date)
        .extra({'month': "to_char(created_at, 'Mon YYYY')"})
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    chart_data = {
        'labels': [item['month'] for item in report_data],
        'reports': [item['count'] for item in report_data],
    }
    
    # Waste types for pie chart
    waste_types = WasteType.objects.annotate(
        count=Count('report')
    ).order_by('-count')
    
    # Color palette for waste types
    colors = [
        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', 
        '#858796', '#5a5c69', '#6f42c1', '#20c9a6', '#36b9cc'
    ]
    hover_colors = [
        '#2e59d9', '#17a673', '#2c9faf', '#dda20a', '#be2617', 
        '#717384', '#484a54', '#5d3ca9', '#17a689', '#2c9faf'
    ]
    
    # Assign colors to waste types
    for i, waste_type in enumerate(waste_types):
        color_index = i % len(colors)
        waste_type.color = colors[color_index]
        waste_type.hover_color = hover_colors[color_index]
    
    # Zone collection efficiency
    efficiency = {
        'north_zone': 78,
        'south_zone': 62,
        'east_zone': 87,
        'west_zone': 91,
        'central_zone': 83,
    }
    
    # Vehicle performance data
    vehicle_performance = Vehicle.objects.filter(active=True).order_by('-collections')[:10]
    for vehicle in vehicle_performance:
        if vehicle.efficiency >= 90:
            vehicle.efficiency_color = 'success'
        elif vehicle.efficiency >= 75:
            vehicle.efficiency_color = 'info'
        elif vehicle.efficiency >= 60:
            vehicle.efficiency_color = 'warning'
        else:
            vehicle.efficiency_color = 'danger'
    
    # Vendor warnings
    warnings = VendorWarning.objects.all().order_by('-created_at')
    for warning in warnings:
        if warning.status == 'pending':
            warning.status_color = 'warning'
        elif warning.status == 'acknowledged':
            warning.status_color = 'info'
        elif warning.status == 'resolved':
            warning.status_color = 'success'
    
    # Vendor performance
    vendors = Vendor.objects.all()
    for vendor in vendors:
        vendor.warnings_count = VendorWarning.objects.filter(vendor=vendor).count()
        vendor.rating = vendor.calculate_rating()  # Assuming a method on the Vendor model
        vendor.rating_percentage = (vendor.rating / 5) * 100
        
        if vendor.rating >= 4:
            vendor.rating_color = 'success'
        elif vendor.rating >= 3:
            vendor.rating_color = 'info'
        elif vendor.rating >= 2:
            vendor.rating_color = 'warning'
        else:
            vendor.rating_color = 'danger'
    
    # All vendors for dropdown in warning modal
    all_vendors = Vendor.objects.all()
    
    context = {
        'stats': stats,
        'campaigns': campaigns,
        'rewards': rewards,
        'top_users': top_users,
        'recent_claims': recent_claims,
        'chart_data': chart_data,
        'waste_types': waste_types,
        'efficiency': efficiency,
        'vehicle_performance': vehicle_performance,
        'warnings': warnings,
        'vendors': vendors,
        'all_vendors': all_vendors,
        'user': request.user,
    }
    
    return render(request, 'municipalview.html', context)

@login_required
@user_passes_test(is_municipal_admin)
def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.created_by = request.user
            campaign.save()
            return redirect('municipal_dashboard')
    return redirect('municipal_dashboard')

@login_required
@user_passes_test(is_municipal_admin)
def create_reward(request):
    if request.method == 'POST':
        form = RewardForm(request.POST, request.FILES)
        if form.is_valid():
            reward = form.save(commit=False)
            reward.created_by = request.user
            reward.save()
            return redirect('municipal_dashboard')
    return redirect('municipal_dashboard')

@login_required
@user_passes_test(is_municipal_admin)
def issue_warning(request):
    if request.method == 'POST':
        form = WarningForm(request.POST)
        if form.is_valid():
            warning = form.save(commit=False)
            warning.issued_by = request.user
            warning.save()
            return redirect('municipal_dashboard')
    return redirect('municipal_dashboard')

@login_required
@user_passes_test(is_municipal_admin)
def download_analytics(request):
    # Create a CSV file
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    
    # Write headers
    writer.writerow(['Date', 'Total Reports', 'Reports Resolved', 'Resolution Rate (%)'])
    
    # Get data for the last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    date_range = [start_date + timedelta(days=x) for x in range(31)]
    
    for date in date_range:
        # Count reports for this date
        total_reports = Report.objects.filter(created_at__date=date).count()
        resolved_reports = Report.objects.filter(created_at__date=date, status='resolved').count()
        
        # Calculate resolution rate
        resolution_rate = 0
        if total_reports > 0:
            resolution_rate = (resolved_reports / total_reports) * 100
        
        # Write row
        writer.writerow([
            date.strftime('%Y-%m-%d'),
            total_reports,
            resolved_reports,
            f"{resolution_rate:.2f}"
        ])
    
    # Create response with CSV
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cleancity_analytics.csv"'
    
    return response

@login_required
@user_passes_test(is_municipal_admin)
def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    return render(request, 'campaign_detail.html', {'campaign': campaign})

@login_required
@user_passes_test(is_municipal_admin)
def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaign_detail', campaign_id=campaign.id)
    else:
        form = CampaignForm(instance=campaign)
    
    return render(request, 'edit_campaign.html', {
        'form': form,
        'campaign': campaign
    })

@login_required
@user_passes_test(is_municipal_admin)
def delete_campaign(request, campaign_id):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, id=campaign_id)
        campaign.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_municipal_admin)
def edit_reward(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id)
    
    if request.method == 'POST':
        form = RewardForm(request.POST, request.FILES, instance=reward)
        if form.is_valid():
            form.save()
            return redirect('municipal_dashboard')
    else:
        form = RewardForm(instance=reward)
    
    return render(request, 'edit_reward.html', {
        'form': form,
        'reward': reward
    })

@login_required
@user_passes_test(is_municipal_admin)
def warning_detail(request, warning_id):
    warning = get_object_or_404(VendorWarning, id=warning_id)
    return render(request, 'warning_detail.html', {'warning': warning})

@login_required
@user_passes_test(is_municipal_admin)
def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    warnings = VendorWarning.objects.filter(vendor=vendor).order_by('-created_at')
    
    context = {
        'vendor': vendor,
        'warnings': warnings,
    }
    
    return render(request, 'vendor_detail.html', context)

@login_required
@user_passes_test(is_municipal_admin)
def approve_claim(request, claim_id):
    if request.method == 'POST':
        claim = get_object_or_404(RewardClaim, id=claim_id, status='pending')
        claim.status = 'approved'
        claim.approved_by = request.user
        claim.approved_at = timezone.now()
        claim.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_municipal_admin)
def reject_claim(request, claim_id):
    if request.method == 'POST':
        claim = get_object_or_404(RewardClaim, id=claim_id, status='pending')
        claim.status = 'rejected'
        claim.approved_by = request.user
        claim.approved_at = timezone.now()
        claim.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
