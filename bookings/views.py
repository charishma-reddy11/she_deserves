from django.shortcuts import render, redirect, get_object_or_404
from .models import Destination, Category # Booking model unte adi kuda add chey

# 1. Home Page
def home(request):
    destinations = Destination.objects.all()
    categories = Category.objects.all()
    return render(request, 'travel/home.html', {'destinations': destinations, 'categories': categories})

# 2. Details Form Page (Confirm Trip)
def book_ride(request, dest_id):
    destination = get_object_or_404(Destination, id=dest_id)
    if destination.seats_filled >= 3:
        return render(request, 'travel/home.html', {'error': 'Seats are full!', 'destinations': Destination.objects.all()})
    
    # Ikkada seat increment cheyakudadhu, just form chupinchali
    return render(request, 'travel/confirm_trip.html', {'destination': destination})

# 3. Payment & Female Verification Logic
def process_payment(request, dest_id):
    destination = get_object_or_404(Destination, id=dest_id)
    
    if request.method == "POST":
        name = request.POST.get('passenger_name')
        is_female = request.POST.get('female_verification') # Checkbox value
        
        # Female verification check
        if not is_female:
            return render(request, 'travel/confirm_trip.html', {
                'destination': destination,
                'error': 'Error: Only female passengers are allowed.'
            })

        if destination.seats_filled < 3:
            destination.seats_filled += 1
            destination.save()
            return render(request, 'travel/payment_success.html', {'destination': destination, 'name': name})
    
    return redirect('travel:home')

# 4. Cancel Ride Logic
def cancel_ride(request, dest_id):
    destination = get_object_or_404(Destination, id=dest_id)
    if destination.seats_filled > 0:
        destination.seats_filled -= 1
        destination.save()
    return redirect('travel:registered_trips')

# 5. Registered Trips
def registered_trips(request):
    booked_destinations = Destination.objects.filter(seats_filled__gt=0)
    return render(request, 'travel/registered_trips.html', {'booked_destinations': booked_destinations})