from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from ledger.models import Agent, Bank, Account, Order, OrderHistory
import random
from ledger import utils

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create fake Agents
        for _ in range(5):
            Agent.objects.create(
                username=fake.user_name(),
                phone_number=fake.phone_number(),
                profile_picture=None  # You can add a default picture or leave it as None
            )

        # Create fake Banks
        bank_names = [bank_names[0] for bank_names in utils.BANKS]
        for name in bank_names:
            Bank.objects.create(
                name=name,
                logo=None  # You can add a default picture or leave it as None
            )

        # Create fake Accounts
        agents = Agent.objects.all()
        banks = Bank.objects.all()
        account_types = [account_types[0] for account_types in utils.ACCOUNT_TYPES]

        for _ in range(10):
            Account.objects.create(
                agent=random.choice(agents),
                bank=random.choice(banks),
                account_number=fake.unique.bban(),
                account_holder_name=fake.name(),
                account_type=random.choice(account_types),
                balance=fake.pydecimal(left_digits=6, right_digits=2, positive=True)
            )

        # Create fake Orders
        accounts = Account.objects.all()
        order_types = [order_type[0] for order_type in utils.ORDER_TYPES]

        for _ in range(30):
            Order.objects.create(
                agent=random.choice(agents),
                created_at=fake.date_this_month(),
                updated_at=fake.date_this_month(),
                name=fake.word(),
                account_number=fake.bban(),
                amount=fake.random_int(min=1000, max=100000),
                order_type=random.choice(order_types),
                credit_bank_account=random.choice(accounts),
            )

        # Create fake OrderHistory
        orders = Order.objects.all()
        for order in orders:
            OrderHistory.objects.create(
                order=order,
                status=random.choice(order_types),
                changed_by=random.choice(agents)
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data'))
