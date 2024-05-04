from django.shortcuts import render

from django.shortcuts import render
from .models import Place
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required


@login_required
def secret_page(request):
    return render(request, 'account.html')


@login_required
def map(request):
    places = serialize('geojson', Place.objects.all())
    return render(request, 'mainMap.html', {'places': places})