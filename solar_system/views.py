from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def galaxy(request):
    return render(request, 'hackathon/galaxy.html')