from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from . import utils


# Create your models here.
class Agent(AbstractUser):
    phone_number = models.CharField(max_length=50, default="")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
    

class Bank(models.Model):
    name = models.CharField(max_length=3, choices=utils.BANKS, default=utils.BANKS[0])
    logo = models.ImageField(upload_to='bank_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_bank_name')
        ]

    def __str__(self):
        return self.name
    

class Account(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=22, unique=True, default=None)
    account_holder_name = models.CharField(max_length=100, default=None)
    account_type = models.CharField(choices=utils.ACCOUNT_TYPES, default=utils.ACCOUNT_TYPES[0])
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_holder_name} - {self.account_number}"
    

class Order(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(auto_now=True)
    name = models.CharField(max_length=20, default=None)
    account_number = models.CharField(max_length=22, default=None)
    amount = models.PositiveIntegerField(default=None)
    commission = models.PositiveSmallIntegerField(default=None, blank=True, null=True)
    order_type = models.CharField(max_length=50, choices=utils.ORDER_TYPES, blank=False, default=utils.PAID_ORDERS)
    credit_bank_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')

    class Meta:
        ordering = ['order_type', 'created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    # def save(self, *args, **kwargs):
    #     if self.amount is not None and self.amount <= 100000:
    #         self.commission = 300
    #         self.amount -= self.commission
    #     elif self.amount <= 250000:
    #         self.commission = 400
    #         self.amount -= self.commission
    #     else:
    #         self.commission = 500
    #         self.amount -= self.commission

    #     super(Order, self).save(*args, **kwargs)

    # # Deduct amount from the selected account if the order type is PAID
    #     if self.order_type == utils.PAID_ORDERS:
    #         account = self.credit_bank_account
    #         if account.balance < self.amount:
    #             raise ValidationError("Insufficient funds in the selected account.")
    #         account.balance -= self.amount
    #         account.save()
    #     elif self.order_type == utils.CANCEL_ORDERS:
    #         account = self.credit_bank_account
    #         account.balance += self.amount
    #         account.save()
    #     elif self.order_type == utils.PENDING_ORDERS:
    #         pass

    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " - " + str(self.account_number)
    

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=50, choices=utils.ORDER_TYPES)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.order.order_type} - {self.status} on {self.changed_at}"


class Expense(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.agent.username} - {self.amount}"