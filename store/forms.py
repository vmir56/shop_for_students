from django import forms
from .models import Product
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    price = forms.DecimalField(
        label="Цена",
        min_value=0.01,
        initial=0.01
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']  # добавил image
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название товара'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Категория товара'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),  # виджет для загрузки
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise ValidationError("Цена не может быть пустой.")
        if price < 0:
            raise ValidationError("Цена должна быть больше нуля.")
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise ValidationError("Название товара не может быть пустым.")
        return name.strip()

