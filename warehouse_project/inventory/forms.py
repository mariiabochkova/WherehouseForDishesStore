from django import forms
from .models import Goods, Department, Suppliers, Invoice, Units, ArrivalDetails
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ['name', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SuppliersForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = ['name', 'contact_person', 'phone', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['data', 'suppliers', 'department']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'suppliers': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }

class UnitsForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = ['name', 'short_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ArrivalDetailsForm(forms.ModelForm):
    class Meta:
        model = ArrivalDetails
        fields = ['goods', 'amount', 'price_for_unit']
        widgets = {
            'goods': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            "price_for_unit": forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': _("Username"),
        }
        help_texts = {
            'username': _("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        }

class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Username")
        if 'password1' in self.fields:
            self.fields['password1'].label = _("Password")
        if 'password2' in self.fields:
            self.fields['password2'].label = _("Password confirmation")

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = _("Old password")
        self.fields['new_password1'].label = _("New password")
        self.fields['new_password2'].label = _("New password confirmation")

class MyLoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Логін"))
    password = forms.CharField(label=_("Пароль"), widget=forms.PasswordInput)