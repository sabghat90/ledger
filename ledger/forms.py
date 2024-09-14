from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *


class LoginForm(AuthenticationForm):
    class Meta:
        model = Agent
        fields = ('username', 'password')


class RegisterForm(UserCreationForm):
    class Meta:
        model = Agent
        fields = ('username', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    
class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('created_at', 'name', 'account_number', 'amount', 'commission', 'order_type', 'credit_bank_account')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['credit_bank_account'].queryset = Account.objects.filter(agent=self.instance.agent)


class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('bank', 'account_number', 'account_holder_name', 'account_type', 'balance')


class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
