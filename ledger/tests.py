from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Agent, Bank, Account, Order, OrderHistory, Expense
from . import utils


class AgentModelTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(username='testuser', phone_number='1234567890')

    def test_agent_creation(self):
        self.assertEqual(self.agent.username, 'testuser')
        self.assertEqual(self.agent.phone_number, '1234567890')

    def test_agent_str(self):
        self.assertEqual(str(self.agent), 'testuser')


class BankModelTest(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(name=utils.BANKS[0])

    def test_bank_creation(self):
        self.assertEqual(self.bank.name, utils.BANKS[0])

    def test_bank_str(self):
        self.assertEqual(str(self.bank), utils.BANKS[0])


class AccountModelTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(username='testuser')
        self.bank = Bank.objects.create(name=utils.BANKS[0])
        self.account = Account.objects.create(
            agent=self.agent,
            bank=self.bank,
            account_number='1234567890123456789012',
            account_holder_name='Test User',
            account_type=utils.ACCOUNT_TYPES[0],
            balance=1000.00
        )

    def test_account_creation(self):
        self.assertEqual(self.account.account_holder_name, 'Test User')
        self.assertEqual(self.account.account_number, '1234567890123456789012')
        self.assertEqual(self.account.balance, 1000.00)

    def test_account_str(self):
        self.assertEqual(str(self.account), 'Test User - 1234567890123456789012')


class OrderModelTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(username='testuser')
        self.bank = Bank.objects.create(name=utils.BANKS[0])
        self.account = Account.objects.create(
            agent=self.agent,
            bank=self.bank,
            account_number='1234567890123456789012',
            account_holder_name='Test User',
            account_type=utils.ACCOUNT_TYPES[0],
            balance=1000.00
        )
        self.order = Order.objects.create(
            agent=self.agent,
            name='Test Order',
            account_number='1234567890123456789012',
            amount=500,
            order_type=utils.PAID_ORDERS,
            credit_bank_account=self.account
        )

    def test_order_creation(self):
        self.assertEqual(self.order.name, 'Test Order')
        self.assertEqual(self.order.amount, 500)
        self.assertEqual(self.order.order_type, utils.PAID_ORDERS)

    def test_order_str(self):
        self.assertEqual(str(self.order), 'Test Order - 1234567890123456789012')


class OrderHistoryModelTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(username='testuser')
        self.bank = Bank.objects.create(name=utils.BANKS[0])
        self.account = Account.objects.create(
            agent=self.agent,
            bank=self.bank,
            account_number='1234567890123456789012',
            account_holder_name='Test User',
            account_type=utils.ACCOUNT_TYPES[0],
            balance=1000.00
        )
        self.order = Order.objects.create(
            agent=self.agent,
            name='Test Order',
            account_number='1234567890123456789012',
            amount=500,
            order_type=utils.PAID_ORDERS,
            credit_bank_account=self.account
        )
        self.order_history = OrderHistory.objects.create(
            order=self.order,
            status=utils.PAID_ORDERS,
            changed_by=self.agent
        )

    def test_order_history_creation(self):
        self.assertEqual(self.order_history.status, utils.PAID_ORDERS)
        self.assertEqual(self.order_history.changed_by, self.agent)

    def test_order_history_str(self):
        self.assertIn(self.order_history.status, str(self.order_history))
        self.assertIn(str(self.order_history.changed_at), str(self.order_history))


class ExpenseModelTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(username='testuser')
        self.bank = Bank.objects.create(name=utils.BANKS[0])
        self.expense = Expense.objects.create(
            agent=self.agent,
            bank=self.bank,
            amount=100.00,
            description='Test Expense'
        )

    def test_expense_creation(self):
        self.assertEqual(self.expense.amount, 100.00)
        self.assertEqual(self.expense.description, 'Test Expense')

    def test_expense_str(self):
        self.assertEqual(str(self.expense), 'testuser - 100.00')