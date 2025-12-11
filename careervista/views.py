from django.shortcuts import render
from careers.models import Career

def home(request):
    featured_careers = Career.objects.all()[:6]
    return render(request, 'home.html', {'featured_careers': featured_careers})
