class PaymentStatus:
    WAITING_FOR_APPROVAL = 0
    APPROVED = 1
    DECLINED = 2

    CHOICES = (
        (WAITING_FOR_APPROVAL, 'Waiting for Approval'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
    )


class TransactionStatus:
    UNVERIFIED = 0
    VERIFIED = 1
    CANCELLED = 2

    CHOICES = (
        (UNVERIFIED, 'Unverified'),
        (VERIFIED, 'Verified'),
        (CANCELLED, 'Cancelled'),
    )


class TransactionType:
    THIRD_PARTY_DEPOSIT = 3
    THIRD_PARTY_WITHDRAW = 4

    CHOICES = (
        (THIRD_PARTY_WITHDRAW, 'Third Party Withdraw'),
        (THIRD_PARTY_DEPOSIT, 'Third Party Deposit'),
    )
