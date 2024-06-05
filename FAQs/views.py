from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def FAQs(request):
    return HttpResponse("This is where my FAQs will be displayed")