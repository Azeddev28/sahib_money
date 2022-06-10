from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .authentication import MerchantAuthentication
from .permissions import IsAuthorizedMerchant
from apps.wallet.models import Wallet
from apps.wallet.choices import TransactionType, TransactionStatus
from apps.third_party_transaction.models import ThirdPartyTransaction, TransactionOTP
from apps.third_party_transaction.utils import get_decoded_transaction_details

User = get_user_model()


class MerchantTransactionViewSet(viewsets.ViewSet):
    authentication_classes = [MerchantAuthentication]
    permission_classes = [IsAuthorizedMerchant]

    def init_withdrawal_transaction(self, request, *args, **kwargs):
        encoded_transaction_details = request.POST.get('transaction_details')
        if not encoded_transaction_details:
            return Response({'error': "Transaction details were not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_email, requested_credits = get_decoded_transaction_details(encoded_transaction_details)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'error': "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # check if another third party transaction is in pipeline from the same user
        try:
            last_transaction = user.wallet.transactions\
                                .select_related('thirdpartytransaction')\
                                .order_by('-created')\
                                .first()
        except Wallet.DoesNotExist:
            return Response({'error': "User wallet does not exist"} ,status=status.HTTP_400_BAD_REQUEST)

        if last_transaction:
            last_transaction = ThirdPartyTransaction.objects.get(uuid=last_transaction.uuid)
            if not last_transaction.is_invalid():
                return Response({'error': "Another transaction is in progress"}, status=status.HTTP_400_BAD_REQUEST)

        # check if requested withdrawal credits are greater than available credits in user wallet
        if requested_credits > user.wallet.total_amount:
            return Response({'error': "User does not have enough credits in the wallet"}, status=status.HTTP_400_BAD_REQUEST)

        transaction_reference = request.POST.get('transaction_reference', '')
        try:
            # create third party withdraw transaction
            transaction = ThirdPartyTransaction.objects.create(
                wallet=user.wallet,
                reference=transaction_reference,
                merchant_account=request.user.merchant_account,
                type=TransactionType.THIRD_PARTY_WITHDRAW,
                amount=requested_credits
            )
        except IntegrityError:
            return Response({'error': "This transaction reference has already been used"}, status=status.HTTP_400_BAD_REQUEST)

        # Changing this part to return otp url
        response = {
            'success': 'Withdrawal transaction inititated',
            'otp_url': f"{settings.SITE_BASE_URL}{reverse('otp_view', args=(transaction.uuid,))}"
        }

        return Response(response)

    def transaction_status(self, request, *args, **kwargs):
        reference = request.POST.get('transaction_reference')
        try:
            transaction = ThirdPartyTransaction.objects.get(reference=reference)
        except ThirdPartyTransaction.DoesNotExist:
            return Response({'error': "Transaction does not exist"})

        return Response({'status': transaction.status})


class CancelWithdrawalTransaction(views.APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        uuid = request.GET.get('uuid')
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            return Response({'error': "Transaction does not exist"})

        if transaction.is_invalid():
            return Response({'error': "Transaction is not valid anymore"})

        transaction.otp.delete()
        transaction.status = TransactionStatus.CANCELLED
        transaction.save()

        return Response({'success': 'Transaction has been cancelled'})


class RegenerateOTP(views.APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        uuid = request.GET.get('uuid')

        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            return Response({'error': "Transaction does not exist"} ,status=status.HTTP_400_BAD_REQUEST)

        if transaction.is_invalid():
            return Response({'error': "Transaction Invalid"}, status=status.HTTP_400_BAD_REQUEST)

        transaction.otp.delete()
        TransactionOTP.objects.create(transaction=transaction)
        return Response({'success': 'OTP has been created'})
