from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
# from django.conf import settings
from django.contrib.auth.decorators import login_required

from products.models import Product
from categories.models import Category
# Create your views here.


@login_required(login_url="/users/login")
def sell(request):
    if request.method == 'POST':
        title = request.POST['title']
        slug=title
        price = request.POST['price']
        quantity = request.POST['quantity']
        description = request.POST['description']
        image = request.FILES['image']
        cat = request.POST['category']
        category=Category.objects.filter(title=cat)
        if Product.objects.filter(title=title).exists():
            messages.error(
                request, 'Product with given title is already present.')
            return redirect('products:sell')
        else:
            product = Product.objects.create(
                title=title,slug=slug, price=price, quantity=quantity, description=description, photo=image, category=category[0])
            product.save()
            messages.success(request, 'Your Product is uploaded')
            return redirect('pages:home')
    else:
        categories = Category.objects.all()
        context = {
            'title': 'Home',
            'categories': categories,
        }
        return render(request, 'product/sell.html',context)
