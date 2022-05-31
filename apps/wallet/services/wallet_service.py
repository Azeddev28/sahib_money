from apps.wallet.models import Wallet, WalletTransaction


class WalletTransactionService:

    # these funcs would be edited to incorporate different withdrawl/deposit types
    def perform_user_account_withdrawl(self, user_wallet, amount, account_no):
        transaction = WalletTransaction.objects.create(from_wallet=user_wallet,
                                                       to_wallet=None,
                                                       transaction_type=WalletTransaction.WITHDRAW,
                                                       amount=amount,
                                                       account_no=account_no
                                                       )
        is_succeeded = self.deduct_amount(user_wallet, transaction.amount)
        return is_succeeded

    def perform_user_account_deposit(self, user_wallet, amount, account_no):
        transaction = WalletTransaction.objects.create(from_wallet=None,
                                                       to_wallet=user_wallet,
                                                       transaction_type=WalletTransaction.DEPOSIT,
                                                       amount=amount,
                                                       account_no=None
                                                       )

    def deposit_amount(self, user_wallet, amount):
        user_wallet.total_amount += amount
        user_wallet.save()

    def deduct_amount(self, user_wallet, amount):
        if user_wallet.total_amount >= amount:
            user_wallet.total_amount -= amount
            user_wallet.save()
            return True

        return False
