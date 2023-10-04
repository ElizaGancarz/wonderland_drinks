from django.http import HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages
from .models import Drink, Like

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def get_last_addedd_cocktails():
    last_added_cocktails = Drink.objects.filter(public=True).order_by('-creation_date')[:6]
    first_half = last_added_cocktails[:3] if len(last_added_cocktails[:3]) >= 2 else None
    second_half = last_added_cocktails[3:] if len(last_added_cocktails[3:]) >= 2 else None
    return first_half, second_half

def home(request):
    if request.method == 'GET':
        last_cocktails1, last_cocktails2 = get_last_addedd_cocktails()
        pined_home = Drink.objects.filter(pin_to_main_page=True, public=True)
        pined_home = pined_home if len(pined_home) > 3 else None

        return render(request, 'home.html',
                  {'last_cocktails1': last_cocktails1, 'last_cocktails2': last_cocktails2, 'pined_home': pined_home, 'display_barmans':True})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET'])


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        drinks = Drink.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredient__product__name__icontains=query)
        ).distinct()
        total_count = drinks.count()
        last_added_cocktails, _ = get_last_addedd_cocktails()

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
    if request.method == 'GET':
        drink = get_object_or_404(Drink, id=drink_id)
        if not drink.public and drink.owner != request.user:
            return HttpResponseForbidden('Ups! Nie masz dostępu do tego drinka.')

        last_added_cocktails, _ = get_last_addedd_cocktails()

        is_user_liked = request.user.is_authenticated and drink.is_liked_by_user(request.user)

        context = {'drink': drink,
                   'last_cocktails1': last_added_cocktails,
                   'is_user_liked': is_user_liked,
                   }

        return render(request, 'cocktail_detail.html', context)
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET'])


@login_required
def like_drink(request, drink_id):
    if request.method == 'POST':
        drink = get_object_or_404(Drink, pk=drink_id)
        like = Like.objects.filter(user=request.user, drink=drink).first()

        if like:
            messages.warning(request, 'Już polubiłeś ten drink!')
        else:
            Like.objects.create(user=request.user, drink=drink)
            drink.likes += 1
            drink.save()
            messages.success(request, 'Drink polubiony!')
        return redirect('detail_cocktail', drink_id)
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


@login_required
def unlike_drink(request, drink_id):
    if request.method == 'POST':
        drink = get_object_or_404(Drink, pk=drink_id)
        like = Like.objects.filter(user=request.user, drink=drink).first()

        if like:
            like.delete()
            drink.likes -= 1
            drink.save()
            messages.success(request, 'Drink odlajkowany.')
        return redirect('detail_cocktail', drink_id)
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])
