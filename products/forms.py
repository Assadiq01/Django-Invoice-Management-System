# 6th

from django import forms
from django.forms import inlineformset_factory

from .models import Product, Image, Variant, Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone_number', 'address']

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['customer', 'title', 'date_created', 'total', 'sub_total', 'deposit', 'balance1', 'balance2']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date_created': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'sub_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance1': forms.NumberInput(attrs={'class': 'form-control'}),
            'balance2': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# class ImageForm(forms.ModelForm):

#    class Meta:
#        model = Image
#        fields = ['product', 'image']
#        widgets = {
#            'product': forms.Select(attrs={'class': 'form-control'}),
#            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#        }

class VariantForm(forms.ModelForm):

    class Meta:
        model = Variant
        fields = ['product', 'quantity', 'description', 'rate', 'amount']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

VariantFormSet = inlineformset_factory(
    Product, Variant, form=VariantForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)

#ImageFormSet = inlineformset_factory(
#    Product, Image, form=ImageForm,
#    extra=1, can_delete=True,
#    can_delete_extra=True
#)
