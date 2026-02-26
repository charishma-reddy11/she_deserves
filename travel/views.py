from django.shortcuts import render, get_object_or_404, redirect
from .models import Destination, Category, Booking 
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# 1. Home Page
def home(request):
    query = request.GET.get('q')
    destinations = Destination.objects.filter(name__icontains=query) if query else Destination.objects.all()
    categories = Category.objects.all()
    return render(request, 'travel/home.html', {
        'destinations': destinations, 
        'categories': categories, 
        'query': query
    })

# 2. Category View
def category_view(request, slug):
    query = request.GET.get('q')
    categories = Category.objects.all()
    if slug == 'all':
        destinations = Destination.objects.filter(name__icontains=query) if query else Destination.objects.all()
        category = None
    else:
        category = get_object_or_404(Category, slug=slug)
        destinations = Destination.objects.filter(category=category, name__icontains=query) if query else Destination.objects.filter(category=category)
    
    return render(request, 'travel/home.html', {
        'destinations': destinations, 
        'categories': categories, 
        'selected_category': category, 
        'query': query
    })

# --- STATIC PAGES ---
def safety_guides(request): return render(request, 'travel/safety_guides.html')
def experience(request): return render(request, 'travel/experience.html')
def help_center(request): return render(request, 'travel/help_center.html')
def privacy(request): return render(request, 'travel/privacy.html')
def terms(request): return render(request, 'travel/terms.html')

# 3. Passenger Details Form
@login_required(login_url='accounts1:login')
def book_ride(request, dest_id):
    destination = get_object_or_404(Destination, id=dest_id)
    if destination.seats_filled >= 3:
        messages.error(request, "Sorry, Seats are full for this destination!")
        return redirect('travel:home')
    return render(request, 'travel/confirm_trip.html', {'destination': destination})

# 4. Process Payment - Creates a new Booking entry for EVERY seat
@login_required(login_url='accounts1:login')
def process_payment(request, dest_id):
    destination = get_object_or_404(Destination, id=dest_id)
    if request.method == "POST":
        passenger_name = request.POST.get('passenger_name', request.user.first_name)
        is_female = request.POST.get('female_verification') 

        if not is_female:
            return render(request, 'travel/confirm_trip.html', {
                'destination': destination,
                'error': 'Verification Failed: Only female passengers are allowed!'
            })

        if destination.seats_filled < 3:
            # Update Total Count
            destination.seats_filled += 1
            destination.save()
            
            # SAVE THE BOOKING DETAILS IN DB
            Booking.objects.create(
                user=request.user,
                destination=destination,
                passenger_name=passenger_name
            )

            return render(request, 'travel/payment_success.html', {
                'destination': destination, 
                'name': passenger_name
            })
    
    return redirect('travel:home')
@login_required(login_url='accounts1:login')
def cancel_ride(request, dest_id): 
    booking = get_object_or_404(Booking, id=dest_id, user=request.user)
    destination = booking.destination
    
    if request.method == "POST":
        if destination.seats_filled > 0:
            destination.seats_filled -= 1
            destination.save()
        
        booking.delete() 
        messages.success(request, f"Booking for {destination.name} cancelled.")
            
    return redirect('travel:registered_trips')
# 6. Registered Trips List - Shows all bookings of the logged in user
@login_required(login_url='accounts1:login')
def registered_trips(request):
    
    user_bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    
    return render(request, 'travel/registered_trips.html', {
        'user_bookings': user_bookings, 
        'categories': Category.objects.all()
    })

# --- OTHERS ---
def newsletter_signup(request):
    if request.method == "POST":
        messages.success(request, "Thank you for joining our Newsletter! 💌")
    return redirect('travel:home')

@login_required(login_url='accounts1:login')
def settings_view(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.save()
        messages.success(request, "Profile updated! ✨")
        return redirect('travel:settings_view')
    return render(request, 'travel/settings.html', {'user': user})

def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('travel:home')