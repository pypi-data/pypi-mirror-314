from django.db import models

from .transactions import ShareMixin, Transaction


class Expiry(Transaction, ShareMixin, models.Model):
    pass
