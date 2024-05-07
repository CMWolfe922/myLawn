from django.shortcuts import render

from django.shortcuts import render
from .models import Place
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from .models import Lawn, Booking, Review, Place


@login_required
def secret_page(request):
    return render(request, 'account.html')


@login_required
def map(request):
    places = serialize('geojson', Place.objects.all())
    return render(request, 'mainMap.html', {'places': places})


@login_required
def home(request):
    lawns = Lawn.objects.all()
    pk = request.GET.get("pk")
    if pk:
        lawn = Lawn.objects.get(pk=pk)
        bookings = Booking.objects.filter(lawn=lawn)
        reviews = Review.objects.filter(lawn=lawn)
        return render(request, "lawn_manager/lawn_detail.html", {"lawn": lawn, "bookings": bookings, "reviews": reviews})
    return render(request, "lawn_manager/home.html", {"lawns": lawns})

def create_booking(request):
    if request.method == "POST":
        lawn = Lawn.objects.get(pk=request.POST.get("lawn"))
        booking = Booking.objects.create(
            lawn=lawn,
            date=request.POST.get("date"),
            start_time=request.POST.get("start_time"),
            end_time=request.POST.get("end_time"),
            customer_name=request.POST.get("customer_name"),
            customer_phone=request.POST.get("customer_phone"),
            customer_email=request.POST.get("customer_email")
        )
        return render(request, "lawn_manager/booking_confirmation.html", {"booking": booking})
    return render(request, "lawn_manager/home.html")

def create_review(request):
    if request.method == "POST":
        lawn = Lawn.objects.get(pk=request.POST.get("lawn"))
        review = Review.objects.create(
            lawn=lawn,
            rating=request.POST.get("rating"),
            comment=request.POST.get("comment")
        )
        return render(request, "lawn_manager/review_confirmation.html", {"review": review})
    return render(request, "lawn_manager/home.html")