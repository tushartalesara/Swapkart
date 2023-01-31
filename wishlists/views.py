from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from products.models import Product
from categories.models import Category
from wishlists.models import WishList


@login_required(login_url="/users/login")
def add_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_id = request.user.id
    wl = WishList(user_id=user_id, product=product)
    wl.save()
    if wl:
        messages.success(request, 'Item added to your wishlist')
        return redirect('/')
    else:
        messages.warning(request, 'SomeThing Went Wrong')
        return redirect('/')

@login_required(login_url="/users/login")
def my_wishlists(request):
    products = WishList.objects.filter(user_id=request.user.id)
    wishlists = []
    categories = Category.objects.all()
    for i in products:
        pro = str(i.product)
        product = Product.objects.get(title=pro)
        wishlists.append({
            "photo": product.photo.url,
            "title": product.title,
            "summary": product.summary,
            "slug": product.slug,
            "id": i.pk
        })
    context = {
        'title': 'My WishList',
        'wishlists': wishlists,
        'categories': categories,
        # 'id':id
    }
    return render(request, 'wishlists/all_wishlists.html', context)


@login_required(login_url="/users/login")
def clear_wishlists(request):
    context = {
        'title': 'My WishList',
    }
    return render(request, 'wishlists/all_wishlists.html', context)


@login_required(login_url="/users/login")
def delete_wishlist(request, wishlist_id):
    wl = WishList.objects.get(pk=wishlist_id)
    wl.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
