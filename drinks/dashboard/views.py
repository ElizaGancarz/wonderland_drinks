import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404

from cocktails.forms import DrinkForm, IngredientFormset
from cocktails.models import Drink


@login_required()
def dashboard(request):
    if request.method == 'GET':
        drinks_user = Drink.objects.filter(
            Q(owner=request.user) |
            Q(like__user=request.user)
        ).distinct().order_by('name')

        paginator = Paginator(drinks_user, 4)
        page_number = request.GET.get('page')

        try:
            drinks_user = paginator.get_page(page_number)
        except PageNotAnInteger:
            drinks_user = paginator.page(1)
        except EmptyPage:
            drinks_user = paginator.page(paginator.num_pages)

        return render(request, 'dashboard.html', {'drinks_user': drinks_user})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET'])


@login_required()
def create_drink(request):
    if request.method == 'GET':
        return render(request, 'create.html', {'drink_form': DrinkForm(), 'ingredient_formset': IngredientFormset()})
    elif request.method == 'POST':
        drink_form = DrinkForm(request.POST, request.FILES)
        ingredients_formset = IngredientFormset(data=request.POST)
        if drink_form.is_valid():
            drink = drink_form.save(commit=False)
            drink.owner = request.user
            ingredients_formset = IngredientFormset(data=request.POST, instance=drink)
            if ingredients_formset.is_valid():
                drink.save()
                ingredients_formset.save()
                messages.success(request, 'Drink został pomyślnie dodany.')
                return redirect('dashboard')
        messages.error(request, 'Popraw poniższe błędy:')
        return render(request, 'create.html', {'drink_form': drink_form, 'ingredient_formset': ingredients_formset})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


@login_required
def edit_drink(request, drink_id):
    drink = get_object_or_404(Drink, pk=drink_id, owner=request.user)

    if request.method == 'GET':
        drink_form = DrinkForm(instance=drink)
        ingredient_formset = IngredientFormset(instance=drink)
        return render(request, 'create.html',
                      {'drink_form': drink_form, 'ingredient_formset': ingredient_formset, 'drink': drink})

    elif request.method == 'POST':
        drink_form = DrinkForm(request.POST, request.FILES, instance=drink)
        ingredient_formset = IngredientFormset(data=request.POST, instance=drink)
        if drink_form.is_valid() and ingredient_formset.is_valid():
            drink_form.save()
            ingredient_formset.save()
            # delete ingredients that were removed from the form
            form_ingredients = [form.instance for form in ingredient_formset]
            for ingredient in drink.ingredients.all():
                if ingredient not in form_ingredients:
                    ingredient.delete()
            messages.success(request, 'Drink został zaktualizowany')
            return redirect('dashboard')
        messages.error(request, 'Popraw poniższe błędy:')
        return render(request, 'create.html',
                      {'drink_form': drink_form, 'ingredient_formset': ingredient_formset, 'drink': drink})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


@login_required()
def delete_drink(request, drink_id):
    if request.method == 'POST':
        drink = get_object_or_404(Drink, pk=drink_id, owner=request.user)
        if os.path.isfile(drink.image.path):
            os.remove(drink.image.path)
        if os.path.isfile(drink.thumbnail.path):
            os.remove(drink.thumbnail.path)
        drink.delete()
        messages.success(request, 'Drink został usunięty z twojej listy')
        return redirect('dashboard')
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])
