class WalletTransactionService:
    @staticmethod
    def deposit_amount(user_wallet, amount):
        user_wallet.total_amount += amount
        user_wallet.save()

    @staticmethod
    def deduct_amount(user_wallet, amount):
        if user_wallet.total_amount >= amount:
            user_wallet.total_amount -= amount
            user_wallet.save()
            return True

        return False
