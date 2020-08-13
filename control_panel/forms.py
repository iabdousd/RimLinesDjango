from django.forms import ModelForm, DateTimeInput
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['date_created']
        widgets = {
            'date_created': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class GiftCardForm(ModelForm):
    class Meta:
        model = GiftCard
        fields = ['product', 'serial', 'code']


class OrderForm(forms.Form):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer_number = forms.CharField(label='Customer Number', max_length=100)
    customer_name = forms.CharField(label='Customer Name', max_length=100)
    from_destination = forms.CharField(label='Money Coming From', max_length=100)
    quantity = forms.IntegerField(label='Quantity')
    product = forms.ModelChoiceField(Product.objects, label='Product')
    method = forms.ModelChoiceField(PaymentMethod.objects, label='Payment Method')
    status = forms.ChoiceField(label='Order Status', choices=STATUS)
    verified = forms.BooleanField(label='Payment Done')

