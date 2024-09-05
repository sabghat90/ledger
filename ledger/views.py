from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import *
from django.contrib.auth import get_user_model
from . import utils
from django.db.models import Sum
from django.contrib.auth.decorators import login_not_required

User = get_user_model()


# Create your views here.
def index(request):
    orders = Order.objects.all()
    accounts = Account.objects.all()

    total_paid_orders_amount = int(
        Order.objects.filter(order_type=utils.PAID_ORDERS, created_at__month=utils.GET_CURRENT_MONTH()).aggregate(Sum('amount'))['amount__sum']) or 0
    total_pending_orders_amount = int(
        Order.objects.filter(order_type=utils.PENDING_ORDERS, created_at__month=utils.GET_CURRENT_MONTH()).aggregate(Sum('amount'))['amount__sum']) or int(0)
    total_cancel_orders_amount = int(
        Order.objects.filter(order_type=utils.CANCEL_ORDERS, created_at__month=utils.GET_CURRENT_MONTH()).aggregate(Sum('amount'))['amount__sum']) or int(0)
    total_orders_for_current_month = int(sum(order.amount for order in orders if order.created_at.month == utils.GET_CURRENT_MONTH())) or 0
    total_commission_for_current_month = int(sum(order.commission or 0 for order in orders if order.created_at.month == utils.GET_CURRENT_MONTH()))
    
    accounts_with_total_orders = []
    for account in accounts:
        total_orders_amount_for_account = Order.objects.filter(credit_bank_account=account).aggregate(Sum('amount'))['amount__sum']
        accounts_with_total_orders.append({
            'account': account,
            'total_orders_amount': total_orders_amount_for_account or 0
        })
    
    context = {
        'total_paid_orders_amount': total_paid_orders_amount,
        'total_pending_orders_amount': total_pending_orders_amount,
        'total_cancel_orders_amount': total_cancel_orders_amount,
        'total_orders_for_current_month': total_orders_for_current_month,
        'accounts_with_total_orders': accounts_with_total_orders,
        'total_commission_for_current_month': total_commission_for_current_month,
        'current_month_name': utils.GET_CURRENT_MONTH_NAME,
        'next_month': utils.GET_NEXT_MONTH_NAME,
    }

    return render(request, 'ledger/index.html', context)


@login_not_required
def register(request):
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

    context = {
        'orders': orders,
        'PENDING': PENDING,
        'PAID': PAID,
        'CANCEL': CANCEL,
    }
    return render(request, 'ledger/orders.html', context)


def add_order(request):
    if request.method == 'POST':
        form = AddOrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order_type = form.cleaned_data['order_type']
            account = form.cleaned_data['credit_bank_account']
            commission = form.cleaned_data['commission'] or utils.calculate_commission(order.amount)
            
            print(commission)
            print(order)
            try:
                if order_type == utils.PAID_ORDERS:
                    account.balance -= order.amount
                    account.balance += commission
                    order.commission = commission
                    order.amount -= commission
                    order.save()
                    account.save()
                    messages.success(request, 'Order added successfully')
                    return redirect('orders')
                    
                elif order_type == utils.PENDING_ORDERS:
                    account.balance -= order.amount
                    account.balance += commission
                    order.commission = commission
                    order.amount -= commission
                    order.save()
                    account.save()
                    messages.success(request, 'Order added successfully')
                    return redirect('orders')
                    
                elif order_type == utils.CANCEL_ORDERS:
                    order.save()
                    messages.success(request, 'Order cancelled successfully')
                    return redirect('orders')
                
            except Account.DoesNotExist:
                return render(request, 'ledger/add_order.html', {'form': form, 'error': 'Account does not exist'})
    else:
        form = AddOrderForm()
    return render(request, 'ledger/add_order.html', {'form': form})


def accounts(request):
    accounts = Account.objects.all()

    context = {
        'accounts': accounts
    }
    return render(request, 'ledger/accounts.html', context)


def add_account(request):
    print("adding account")
    if request.method == 'POST':
        form = AddAccountForm(request.POST)
        if form.is_valid():
            form.save()
            print("added")
            return redirect('accounts')
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
            if form.cleaned_data['order_type'] == utils.PAID_ORDERS:
                
                account.balance -= order.amount
                account.balance += commission
                order.commission = commission

            elif form.cleaned_data['order_type'] == utils.CANCEL_ORDERS:
                account.balance += order.amount
                order.commission = commission
                account.balance += commission

            elif form.cleaned_data['order_type'] == utils.PENDING_ORDERS:
                
                account.balance -= order.amount
                account.balance += commission
                order.commission = commission

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
    expenses = Expense.objects.all()
    return render(request, 'ledger/expense.html', {'expenses': expenses})


def add_expense(request):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        expense_amount = form.cleaned_data['amount']
        if form.is_valid():
            expense = form.save(commit=False)
            account = form.cleaned_data['bank']
            if account.balance < expense_amount:
                return render(request, 'ledger/add_expense.html', {'form': form, 'error': 'Insufficient balance'})
            account.balance -= expense_amount
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


def view_agent(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    orders = Order.objects.filter(agent=agent)

    context = {
        'agent': agent,
        'orders': orders,
    }
    return render(request, 'ledger/view_agent.html', context)