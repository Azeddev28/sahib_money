from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .authentication import MerchantAuthentication
from .permissions import IsAuthorizedMerchant
from apps.wallet.models import Wallet
<<<<<<< HEAD
from apps.wallet.choices import TransactionType, TransactionStatus
from apps.third_party_transaction.models import ThirdPartyTransaction
=======
from apps.wallet.choices import TransactionType
from apps.third_party_transaction.models import ThirdPartyTransaction, TransactionOTP
>>>>>>> 6d3659c904e65aaecfdb69ded4cfa92de207a539
from apps.third_party_transaction.utils import get_decoded_transaction_details

User = get_user_model()


class MerchantTransactionViewSet(viewsets.ViewSet):
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
            if not last_transaction.is_invalid():
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


class CancelWithdrawalTransaction(views.APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        uuid = request.GET.get('uuid')
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            return Response({'message': "Transaction does not exist"})

        if transaction.is_invalid():
            return Response({'message': "Transaction is not valid anymore"})

        transaction.otp.delete()
        transaction.status = TransactionStatus.CANCELLED
        transaction.save()

        return Response({'message': 'Transaction has been cancelled'})


class RegenerateOTP(views.APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        uuid = request.GET.get('uuid')

        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            return Response("Transaction does not exist",status=status.HTTP_400_BAD_REQUEST)

        if transaction.is_invalid():
            return Response("Transaction Invalid",status=status.HTTP_400_BAD_REQUEST)

        transaction.otps.objects.all().delete()
        otp = TransactionOTP.objects.create(transaction=transaction)
        #email code

        return Response({'message': 'success', 'otp': otp})
