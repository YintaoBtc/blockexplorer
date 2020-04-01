import uuid 
from django.db import models
from django.urls import reverse


class Block(models.Model):
    id = models.UUIDField( 
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    hash_block = models.CharField(max_length=200)
    confirmations = models.CharField(max_length=200)
    datetime = models.DecimalField(max_digits=6, decimal_places=2)
    height = models.CharField(max_length=200)
    number_txs = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=200)
    bits = models.CharField(max_length=200)
    weight = models.CharField(max_length=200)
    nonce = models.CharField(max_length=200)

    def __str__(self):
        return self.hash_block

    def get_absolute_url(self):
        return reverse('block_detail', args=[str(self.id)])