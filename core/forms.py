#!/usr/bin/python
# - *- coding: utf- 8 - *-

from django import forms

from core.models import Order, ContactFormSubmissions

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.DecimalField(required=True, decimal_places=0, label='')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class Billing_Form(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['user', 'total_price', 'quantity']


class ContactFormSubmissionsForm(forms.ModelForm):

    class Meta:
        model = ContactFormSubmissions
        fields = "__all__"
