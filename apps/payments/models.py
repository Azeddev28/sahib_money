from django.db import models

# Create your models here.
class Payment(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    receipt = models.ImageField(upload_to='receipts')

    def __repr__(self):
        return 'Payment(%s, %s)' % (self.email, self.file)

    def __str__ (self):
        return self.email
