import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cocktails.models import Drink, Ingredient
from django.http import HttpResponseNotAllowed
from .forms import DrinkForm, IngredientFormset
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.http import Http404
from django.contrib import messages



@login_required()
def dashboard(request):
    drinks_user = Drink.objects.filter(owner=request.user).order_by('name')


    paginator = Paginator(drinks_user, 4)
    page_number = request.GET.get('page')

    try:
        drinks_user = paginator.get_page(page_number)
    except PageNotAnInteger:
        drinks_user = paginator.page(1)
    except EmptyPage:
        drinks_user = paginator.page(paginator.num_pages)

    return render(request, 'dashboard.html', {'drinks_user': drinks_user})


@login_required()
def create(request):
    if request.method == 'GET':
        return render(request, 'create.html', {'drink_form': DrinkForm(), 'ingredient_formset': IngredientFormset()})

    elif request.method == 'POST':
        drink_form = DrinkForm(request.POST, request.FILES)
        ingredients_formset = IngredientFormset(data=request.POST)
        if drink_form.is_valid():
            drink = drink_form.save(commit=False)
            if 'image' in request.FILES:
                drink.image = request.FILES['image']
            drink.owner = request.user
            ingredients_formset = IngredientFormset(data=request.POST, instance=drink)
            if ingredients_formset.is_valid():
                drink.save()
                ingredients_formset.save()
                return redirect('dashboard')
        return render(request, 'create.html', {'drink_form': drink_form, 'ingredient_formset': ingredients_formset})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


@login_required()
def delete_drink(request, postId):
    try:
        drink = Drink.objects.get(pk=postId)
        os.remove(drink.image.path)
        os.remove(drink.thumbnail.path)

        drink.delete()

        messages.success(request, 'Drink został usunięty z twojej listy')

        return redirect('dashboard')

    except Drink.DoesNotExist:
        raise Http404("Wpis nie istnieje")

