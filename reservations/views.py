from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_reservation(request):
    return HttpResponse("This is the reservation page")
