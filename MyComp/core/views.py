from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import Coalesce
from shop.models import Product

# Create your views here.
def render_core(request):

    context = {
        "products": Product.objects.annotate(popularity=Coalesce(Sum('orderlog__count'), 0)).order_by('-popularity')[:3]
    }

    return render(request, "index.html", context=context)

def render_contacts(request):

    return render(request, "contacts.html")