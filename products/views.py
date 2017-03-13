from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def details(request, product_id):

    return HttpResponse("You're looking at product %s." % product_id)
def index(request):
    return HttpResponse("welcome in products")