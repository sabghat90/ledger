from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.template import RequestContext
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import *
from django.contrib.auth import get_user_model
from . import utils
from django.db.models import Sum
from django.db import IntegrityError
from django.contrib.auth.decorators import login_not_required
from .filters import OrderFilter

User = get_user_model()


def aget_object_or_404(request, **kwargs):
    return render(request, '404.html', status=404)

def index(request):
    accounts = Account.objects.filter(agent=request.user)

    total_paid_orders_amount = Order.objects.filter(agent=request.user, order_type=utils.PAID_ORDERS).aggregate(Sum('amount'))['amount__sum'] or 0
    total_pending_orders_amount = Order.objects.filter(agent=request.user, order_type=utils.PENDING_ORDERS).aggregate(Sum('amount'))['amount__sum'] or 0
    total_cancel_orders_amount = Order.objects.filter(agent=request.user, order_type=utils.CANCEL_ORDERS).aggregate(Sum('amount'))['amount__sum'] or 0
    current_month_paid_orders_amount = Order.objects.filter(agent=request.user, order_type=utils.PAID_ORDERS, created_at__month=utils.GET_CURRENT_MONTH()).aggregate(Sum('amount'))['amount__sum'] or 0
    total_commission = Order.objects.filter(agent=request.user, order_type=utils.PAID_ORDERS).aggregate(Sum('commission'))['commission__sum'] or 0

    accounts_with_total_orders = [
        {
            'account': account,
            'total_orders_amount': Order.objects.filter(credit_bank_account=account).aggregate(Sum('amount'))['amount__sum'] or 0
        }
        for account in accounts
    ]

    context = {
        'accounts_with_total_orders': accounts_with_total_orders,
        'current_month': utils.GET_CURRENT_MONTH_NAME,
        'next_month': utils.GET_NEXT_MONTH_NAME,
        'total_paid_orders_amount': total_paid_orders_amount,
        'total_pending_orders_amount': total_pending_orders_amount,
        'total_cancel_orders_amount': total_cancel_orders_amount,
        'current_month_paid_orders_amount': current_month_paid_orders_amount,
        'total_commission': total_commission,
    }

    return render(request, 'ledger/index.html', context)


@login_not_required
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_not_required
def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')  # Redirect to a page after successful login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        return redirect('login')
    return render(request, 'logout.html')


def orders(request):
    orders = Order.objects.all()
    PENDING = utils.PENDING_ORDERS
    PAID = utils.PAID_ORDERS
    CANCEL = utils.CANCEL_ORDERS

    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    context = {
        'orders': orders,
        'PENDING': PENDING,
        'PAID': PAID,
        'CANCEL': CANCEL,
        'order_filter': order_filter
    }
    return render(request, 'ledger/orders.html', context)


def add_order(request):
    if request.method == 'POST':
        form = AddOrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.agent = request.user
            print(order.agent)
            order_type = form.cleaned_data['order_type']
            account = form.cleaned_data['credit_bank_account']
            commission = form.cleaned_data['commission'] or utils.calculate_commission(order.amount)
            
            print(commission)
            print(order)
            try:
                if order_type in [utils.PAID_ORDERS, utils.PENDING_ORDERS]:
                    account.balance -= order.amount
                    account.balance += commission
                    order.commission = commission
                    order.amount -= commission
                elif order_type == utils.CANCEL_ORDERS:
                    order.commission = commission

                order.save()
                account.save()
                messages.success(request, 'Order added successfully')
                return redirect('orders')
                
            except Account.DoesNotExist:
                return render(request, 'ledger/add_order.html', {'form': form, 'error': 'Account does not exist'})
    else:
        form = AddOrderForm()
    return render(request, 'ledger/add_order.html', {'form': form})


def accounts(request):
    accounts = Account.objects.filter(agent=request.user)

    context = {
        'accounts': accounts
    }
    return render(request, 'ledger/accounts.html', context)


def add_account(request):
    if request.method == 'POST':
        form = AddAccountForm(request.POST)
        if form.is_valid():
            try:
                account = form.save(commit=False)
                account.agent = request.user
                account.save()
                return redirect('accounts')
            except IntegrityError:
                print('error')
                form.add_error(None, 'This account is already added.')
    else:
        form = AddAccountForm()
    return render(request, 'ledger/add_account.html', {'form': form})


def view_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    orders = Order.objects.filter(credit_bank_account=account)
    PENDING = utils.PENDING_ORDERS
    PAID = utils.PAID_ORDERS
    CANCEL = utils.CANCEL_ORDERS

    context = {
        'account': account,
        'orders': orders,
        'PENDING': PENDING,
        'PAID': PAID,
        'CANCEL': CANCEL
    }

    return render(request, 'ledger/view_account.html', context)


def view_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    context = {
        'order': order
    }
    return render(request, 'ledger/view_order.html', context)


def update_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = AddOrderForm(request.POST, instance=order)

        if form.is_valid():
            order = form.save(commit=False)
            account = form.cleaned_data['credit_bank_account']
            commission = form.cleaned_data['commission'] or utils.calculate_commission(order.amount)
            order_type = form.cleaned_data['order_type']

            def update_account_balance_and_commission(order, account, commission, order_type):
                if order_type in [utils.PAID_ORDERS, utils.PENDING_ORDERS]:
                    account.balance -= order.amount
                    account.balance += commission
                    order.commission = commission
                elif order_type == utils.CANCEL_ORDERS:
                    account.balance += order.amount
                    order.commission = commission
                    account.balance += commission

            update_account_balance_and_commission(order, account, commission, order_type)

            order.save()
            account.save()
            return redirect('orders')
    else:
        form = AddOrderForm(instance=order)
    return render(request, 'ledger/add_order.html', {'form': form})


def update_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    form = AddAccountForm(request.POST or None, instance=account)
    if form.is_valid():
        form.save()
        return redirect('accounts')
    return render(request, 'ledger/add_account.html', {'form': form})


def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('orders')


def expense(request):
    expenses = Expense.objects.filter(agent=request.user)
    return render(request, 'ledger/expense.html', {'expenses': expenses})


def add_expense(request):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        
        if form.is_valid():
            expense = form.save(commit=False)
            expense_amount = form.cleaned_data['amount']
            account = form.cleaned_data['account']
            if account.balance < expense_amount:
                return render(request, 'ledger/add_expense.html', {'form': form, 'error': 'Insufficient balance'})
            account.balance -= expense_amount
            expense.agent = request.user
            account.save()
            expense.save()
            return redirect('expense')
    else:
        form = AddExpenseForm()
    return render(request, 'ledger/add_expense.html', {'form': form})


def view_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    context = {
        'expense': expense
    }
    return render(request, 'ledger/view_expense.html', context)


def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    form = AddExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('expense')
    return render(request, 'ledger/add_expense.html', {'form': form})


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.bank.balance += expense.amount
    expense.bank.save()
    expense.delete()
    return redirect('expense')


def agents(request):
    agents = Agent.objects.all()
    
    context = {
        'agents': agents
    }
    return render(request, 'ledger/agents.html', context)


def profile(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    orders = Order.objects.filter(agent=agent)
    total_orders = Order.objects.filter(agent=agent).count()
    total_paid_orders = Order.objects.filter(agent=agent, order_type=utils.PAID_ORDERS).count()
    total_paid_orders_amount = Order.objects.filter(agent=agent, order_type=utils.PAID_ORDERS).aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid_orders_commission = Order.objects.filter(agent=agent, order_type=utils.PAID_ORDERS).aggregate(Sum('commission'))['commission__sum'] or 0
    
    context = {
        'agent': agent,
        'orders': orders,
        'total_orders': total_orders,
        'total_paid_orders': total_paid_orders,
        'total_paid_orders_amount': total_paid_orders_amount,
        'total_paid_orders_commission': total_paid_orders_commission,
    }
    return render(request, 'ledger/profile.html', context)
