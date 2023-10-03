from django import forms
from django.forms import inlineformset_factory

from cocktails.models import Drink, Ingredient, Product, UnitType


class DrinkForm(forms.ModelForm):
    name = forms.CharField(
        label='Nazwa drinka',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    description = forms.CharField(
        label='Krótki opis',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    image = forms.ImageField(
        label='Dodaj zdjęcie',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
    )

    public = forms.BooleanField(
        label='Opublikuj',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox-class'}),
    )

    class Meta:
        model = Drink
        fields = ['name', 'description', 'image', 'public']


class IngredientForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label='Produkt',
    )
    amount = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=10000,
        step_size=1,
        label='Ilość',
    )
    unit = forms.ModelChoiceField(
        queryset=UnitType.objects.all(),
        label='Jednostka',
    )
    id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = Ingredient
        fields = ['product', 'amount', 'unit']


IngredientFormset = inlineformset_factory(
        Drink,
        Ingredient,
        fields=['product', 'amount', 'unit', 'id'],
        absolute_max=30,
        max_num=30,
        min_num=1,
        form=IngredientForm,
        extra=0,
        can_delete=False,
        can_delete_extra=False,
    )