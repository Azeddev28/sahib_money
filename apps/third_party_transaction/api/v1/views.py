from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import viewsets, status

from .authentication import MerchantAuthentication
from .permissions import IsAuthorizedMerchant
from apps.wallet.models import Wallet
from apps.wallet.choices import TransactionType
from apps.third_party_transaction.models import ThirdPartyTransaction
from apps.third_party_transaction.utils import get_decoded_transaction_details

User = get_user_model()


class TPTransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = [MerchantAuthentication]
    permission_classes = [IsAuthorizedMerchant]

    def init_withdrawal_transaction(self, request, *args, **kwargs):
        encoded_transaction_details = request.POST.get('transaction_details')
        if not encoded_transaction_details:
            return Response("Transaction details were not provided", status=status.HTTP_400_BAD_REQUEST)

        try:
            user_email, requested_credits = get_decoded_transaction_details(encoded_transaction_details)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response("User does not exist",status=status.HTTP_400_BAD_REQUEST)

        # check if another third party transaction is in pipeline from the same user
        try:
            last_transaction = user.wallet.transactions\
                                .select_related('thirdpartytransaction')\
                                .order_by('-created')\
                                .first()
        except Wallet.DoesNotExist:
            return Response("User wallet does not exist",status=status.HTTP_400_BAD_REQUEST)

        if last_transaction:
            last_transaction = ThirdPartyTransaction.objects.get(uuid=last_transaction.uuid)
            if not last_transaction.has_expired:
                return Response("Another transaction is in progress",status=status.HTTP_400_BAD_REQUEST)

        # check if requested withdrawal credits are greater than available credits in user wallet
        if requested_credits > user.wallet.total_amount:
            return Response("User does not have enough credits in the wallet",status=status.HTTP_400_BAD_REQUEST)

        # create third party withdraw transaction
        transaction = ThirdPartyTransaction.objects.create(
            wallet=user.wallet,
            merchant_account=request.user.merchant_account,
            type=TransactionType.THIRD_PARTY_WITHDRAW,
            amount=requested_credits
        )

        response = {
            'message': 'Withdrawal transaction inititated',
            'uuid': transaction.uuid
        }

        return Response(response)
