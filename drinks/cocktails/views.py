from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from .models import Drink, Like, Ingredient
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    last_added_cocktails = Drink.objects.filter(drink_publish=True).order_by('-creation_date')[:6]
    first_half = last_added_cocktails[:3] if len(last_added_cocktails[:3]) >= 2 else None
    second_half = last_added_cocktails[3:] if len(last_added_cocktails[3:]) >= 2 else None
    pined_home = Drink.objects.filter(pin_to_main_page=True, drink_publish=True)
    pined_home = pined_home if len(pined_home) > 1 else None

    return render(request, 'home.html',
                  {'last_cocktails1': first_half, 'last_cocktails2': second_half, 'pined_home': pined_home, 'display_barmans':True})


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        drinks = Drink.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredient__product__name__icontains=query)
        ).distinct()
        total_count = drinks.count()
        last_added_cocktails = Drink.objects.filter(drink_publish=True).order_by('-creation_date')
        last_added_cocktails = last_added_cocktails[:3] if len(last_added_cocktails[:3]) >= 2 else None

        paginator = Paginator(drinks, 8)
        page_number = request.GET.get('page')

        try:
            drinks = paginator.get_page(page_number)
        except PageNotAnInteger:
            drinks = paginator.page(1)
        except EmptyPage:
            drinks = paginator.page(paginator.num_pages)

        context = {'drinks': drinks, 'last_cocktails1': last_added_cocktails, 'query': query, 'total_count': total_count}

        return render(request, 'search_results.html', context)
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET'])


def detail_cocktail(request, drink_id):
    drink = get_object_or_404(Drink, id=drink_id)
    last_added_cocktails = Drink.objects.filter(drink_publish=True).order_by('-creation_date')
    last_added_cocktails = last_added_cocktails[:3] if len(last_added_cocktails) >= 2 else None

    is_user_liked = False
    if request.user.is_authenticated:
        likes = drink.like_set.filter(user=request.user)
        if likes.exists():
            is_user_liked = True

    context = {'drink': drink,
               'last_cocktails1': last_added_cocktails,
               'is_user_liked': is_user_liked,
               }

    return render(request, 'cocktail_detail.html', context)


@login_required
def like_drink(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)

    like = Like.objects.filter(user=request.user, drink=drink).first()

    if not like:
        Like.objects.create(user=request.user, drink=drink)
        drink.likes += 1
        drink.save()

    return redirect('detail_cocktail', drink_id)


@login_required
def unlike_drink(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id)

    like = Like.objects.filter(user=request.user, drink=drink).first()

    if like:
        like.delete()
        drink.likes -= 1
        drink.save()

    return redirect('detail_cocktail', drink_id)
