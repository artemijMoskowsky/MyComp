from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.db.models import Sum, F, Q
from django.db.models.functions import Coalesce
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from .forms import OrderForm
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

def send_to_telegram(message):
    token = os.getenv("tg_token")
    chat_id = "5328331748"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=payload)

# Create your views here.
def render_catalog(request: HttpRequest):

    category = request.GET.get("category", "all")
    price = request.GET.get("price", "popular")
    search = request.GET.get("search", "")

    products = Product.objects.all()

    if category != "all":
        products = Product.objects.filter(category__name=category)
    
    if price == "popular":
        products = products.annotate(popularity=Coalesce(Sum('orderlog__count'), 0)).order_by('-popularity')
    elif price == "cheap":
        products = products.order_by("price")
    elif price == "expensive":
        products = products.order_by("-price")

    words = search.split()
    for word in words:
        products = products.filter(
            Q(name__icontains = word) | Q(tags__name__icontains = word)
        )

    products = products.distinct()

    context = {
        "products": products
    }

    return render(request, "catalog.html", context=context)

def render_product(request, id: int):
    product = Product.objects.get(id=id)
    context = {
        "product": product,
        "similarities": Product.objects.filter(category=product.category).filter(tags__in=product.tags.all()).exclude(id=product.id).distinct()[:3]
    }
    
    return render(request, "product.html", context=context)


@login_required
@csrf_exempt
def add_to_basket(request: HttpRequest, id:int):
    try:
        product = Product.objects.get(id=id)
        if len(Basket.objects.filter(user=request.user, product=product)):
            basket = Basket.objects.get(user=request.user, product=product)
            basket.count += 1
            if basket.count > product.count:
                basket.count = product.count
            basket.save()
        else:
            basket = Basket.objects.create(
                product = product,
                user = request.user,
                count = 1
            )
    except Exception as _ex:
        print(_ex)
        return HttpResponse("failure", status=403)

    return HttpResponse("success", status=200)

@login_required
@csrf_exempt
def render_basket(request: HttpRequest):

    if request.method == "POST":
        for key in request.POST:
            if key.startswith("products"):
                # print(request.POST.get(key))
                obj = json.loads(request.POST.get(key))
                # print(obj)
                basket = Basket.objects.get(id=obj["basketId"])
                if basket.count != obj["count"]:
                    basket.count = obj["count"]
                    basket.save()
        return HttpResponse(reverse_lazy("placing_order"), status=200)
                

    baskets = Basket.objects.filter(user=request.user)

    context = {
        "baskets": baskets,
        "orders_count": baskets.aggregate(Sum('count'))['count__sum'] or 0,
        "orders_price": baskets.aggregate(sum=Sum(F("product__price") * F("count")))["sum"] or 0
    }
    return render(request, "basket.html", context=context)

@login_required
def render_placing_order(request: HttpRequest):
    form = OrderForm()
    baskets = Basket.objects.filter(user=request.user)
    if len(baskets) == 0:
        return redirect("basket")
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            for basket in baskets:
                order_log = OrderLog.objects.create(product=basket.product, count=basket.count)
                order = Order.objects.create(
                    log = order_log,
                    user = request.user,
                    fullname = form.cleaned_data["fullname"],
                    phone_number = form.cleaned_data["phone_number"],
                    type_of_delivery = form.cleaned_data["type_of_delivery"],
                    type_of_payment = form.cleaned_data["type_of_payment"],
                    city = form.cleaned_data["city"],
                    postoffice = form.cleaned_data["postoffice"]
                )
                send_to_telegram(order)
                basket.delete()

            return redirect("basket")

    context = {
        "form": form,
        "baskets": baskets,
        "orders_price": baskets.aggregate(sum=Sum(F("product__price") * F("count")))["sum"] or 0
    }
    return render(request, "placing_order.html", context=context)

@csrf_exempt
@login_required
def delete_basket(request: HttpRequest, id: int):
    try:
        basket = Basket.objects.get(id=id)
        if basket.user.id == request.user.id:
            basket.delete()
            return HttpResponse("success", status=200)
    except:
        pass
    return HttpResponse("fail", status=403)