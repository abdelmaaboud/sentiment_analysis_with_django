from  ReviewsAnalyser import Analyser
from aspectExtractor import Aspect
from django.shortcuts import render
from .models import Product,Review
from django.http import HttpResponse
from extractbiword import biword
# Create your views here.

def details(request, product_id):
    try:
        product= Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return HttpResponse("<h1>this is not exist </h1>")
    # will change it with product page
    reviews = list(Review.objects.values_list('text',flat=True).filter(product=product))
    print(reviews)

    aspect = biword(reviews)
    aspect_list = aspect.Extract()

    analyser = Analyser(reviews, aspect_list)
    d = analyser.analyse_reviews()
    print(d)

    l_keys = list(d.keys())
    d2=dict()
    l_keys=list()
    l_keys=list(d.keys())
    print("l_keys",l_keys)
    d2=list(d.values())
    print("d2",d2)

    pos=[]
    neg=[]
    count=[]
    special_list=[]
    for i in range(len(l_keys)):
         count.append(i)
    for i in d2:
        pos.append(i["pos"])
        neg.append(i["neg"])
    for i in range(len(l_keys)):
        special_list.append([l_keys[i].lower(),pos[i],neg[i]])

    print(special_list)
    return render(request,'product.html',{'product':product,'reviews':reviews,'special_list':special_list})

def index(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

