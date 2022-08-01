from apps.wallet.models import WithdrawalTransaction
from apps.third_party_transaction.models import ThirdPartyTransaction
from apps.wallet.choices import PaymentStatus, TransactionStatus, TransactionType


def get_withdrawal_transaction_amount(user):
    withdrawal_transactions = WithdrawalTransaction.objects.filter(
        wallet=user.wallet,
        status=PaymentStatus.WAITING_FOR_APPROVAL,
    )
    tp_withdrawal_transactions = ThirdPartyTransaction.objects.filter(
        wallet=user.wallet,
        type=TransactionType.THIRD_PARTY_WITHDRAW,
        status=TransactionStatus.VERIFIED,
        payment_status=PaymentStatus.WAITING_FOR_APPROVAL,
    )
    total_credits = 0
    for transaction in withdrawal_transactions:
        total_credits += transaction.amount

    for transaction in tp_withdrawal_transactions:
        total_credits += transaction.amount

    return total_credits


def get_available_credits(user):
    return user.wallet.total_amount - get_withdrawal_transaction_amount(user)
