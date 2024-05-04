from django.shortcuts import render

from django.shortcuts import render
from .models import Place
from django.core.serializers import serialize

def map(request):
    places = serialize('geojson', Place.objects.all())
    return render(request, 'map.html', {'places': places})