from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, blank = False)
    creation_date = models.DateTimeField(auto_now_add=True, blank = False)
    balance_amount = models.IntegerField(blank = False)
    email = models.EmailField(max_length = 254, blank = False)
    password = models.CharField(max_length=100, blank = False)

class Transactions(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    date_transaction = models.DateTimeField(auto_now_add=True, blank = False)
    amount_changed = models.IntegerField()
    type_of_transaction = models.CharField(max_length=100)
    final_amount = models.IntegerField()