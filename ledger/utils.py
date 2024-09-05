import os
from datetime import datetime

PENDING_ORDERS = "PENDING"
PAID_ORDERS = "PAID"
CANCEL_ORDERS = "CANCEL"

ORDER_TYPES = [
    (PENDING_ORDERS, "Pending Order"),
    (PAID_ORDERS, "Paid Order"),
    (CANCEL_ORDERS, "Cancel Order")
]

BANKS = [
    ("HBL", "Habib Bank Ltd"),
    ("UBL", "United Bank Ltd"),
    ("MBL", "Meezan Bank Ltd"),
    ("ABL", "Allied Bank Ltd"),
]

ACCOUNT_TYPES = [
    ('SAVINGS', 'Savings Account'),
    ('CURRENT', 'Current Account'),
    ('FIXED', 'Fixed Deposit'),
]

GET_CURRENT_MONTH = lambda: datetime.now().month
GET_CURRENT_MONTH_NAME = lambda: datetime.now().strftime('%B')
GET_NEXT_MONTH_NAME = lambda: (datetime.now().replace(month=datetime.now().month + 1)).strftime('%B')

def calculate_commission(amount):
    if amount < 100000:
        return 300
    elif amount < 250000:
        return 400
    else:
        return 500