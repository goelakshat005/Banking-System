from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
import pandas as pd
import numpy as np

from pandas import date_range
from .serializers import User_Serializer, Transactions_Serializer
from .models import User, Transactions

from django.core.mail import send_mail
from django.core.mail import EmailMessage
import datetime

@api_view(['GET','POST','PUT'])
def creation_updation(request):
    if request.method == 'GET':
        manager = User.objects.filter(name='MANAGER')
        if len(manager) == 0:
            User.objects.create(
                name = 'MANAGER',
                email = 'manager123@bank.com',
                balance_amount = 0,
                password = 'manager@123'
            )

        return Response('Welcome to the Bank!')

    elif request.method == 'POST':           # To create new user
        user_data = request.data
        # u1 = User(name='johny1', balance_amount=0, email = 'goelakshat005@gmail.com')
        # u1.save()
        all_users = User.objects.values()
        found = 0
        for user in all_users:
            if user['email'] == request.data['email']:
                found = 1
                return Response('Email Id already links to some other account holder!')
        
        User.objects.create(
            name = request.data['name'],
            email = request.data['email'],
            balance_amount = request.data['balance_amount'],
            password = request.data['password']
        )
        data = User.objects.filter(email=request.data['email']).values('id','name','email','balance_amount')
 
        message_body = 'Dear Sir/Ma\'am, \n\nWelcome to the bank! An amount of ' + str(request.data['balance_amount']) + ' has been deposited into your account number ' + str(data[0]['id']) + ' just now. Your final amount is: '+ str(request.data['balance_amount']) +'\n\nThanks & Regards'
        mail = EmailMessage('Congratulations on your new account!', message_body, 'akshattesting@gmail.com', [data[0]['email']])
        mail.send()        
        
        return Response(data)

        # {"name":"akshat goel",
        # "email":"goelakshat005@gmail.com",
        # "balance_amount":50000,
        # "password":"12345"}
    
    elif request.method == 'PUT':   # For withdrawal or deposit
        user_data_object = User.objects.filter(email=request.data['email'])  # we can do this with the 'id' created in the User table as well
        user_data = User.objects.filter(email=request.data['email']).values()
        
        if request.data['type_of_transaction'] == 'Withdrawal' and request.data['password'] == user_data[0]['password']:
            Transactions.objects.create(
                email = user_data_object[0],
                amount_changed = request.data['amount_changed'],
                type_of_transaction = request.data['type_of_transaction'],
                final_amount = user_data[0]['balance_amount'] - request.data['amount_changed']
            )
            balance_amount = user_data[0]['balance_amount']-request.data['amount_changed']
            User.objects.filter(email=request.data['email']).update(balance_amount=balance_amount)

            message_body = 'Dear Sir/Ma\'am, \n\nAn amount of ' + str(request.data['amount_changed']) + ' has been deducted from your account number ' + str(user_data[0]['id']) + ' just now. Your final amount is: '+ str(balance_amount) +'\n\nThanks & Regards'
            mail = EmailMessage('Latest Transaction Activity in your account', message_body, 'akshattesting@gmail.com', [user_data[0]['email']])
            mail.send()

        elif request.data['type_of_transaction'] == 'Deposit' and request.data['password'] == user_data[0]['password']:
            Transactions.objects.create(
                email = user_data_object[0],
                amount_changed = request.data['amount_changed'],
                type_of_transaction = request.data['type_of_transaction'],
                final_amount = user_data[0]['balance_amount'] + request.data['amount_changed']
            )
            balance_amount = user_data[0]['balance_amount']+request.data['amount_changed']
            User.objects.filter(email=request.data['email']).update(balance_amount=balance_amount)
    
            message_body = 'Dear Sir/Ma\'am, \n\nAn amount of ' + str(request.data['amount_changed']) + ' has been deposited into your account number ' + str(user_data[0]['id']) + ' just now. Your final amount is: '+ str(balance_amount) +'\n\nThanks & Regards'
            mail = EmailMessage('Latest Transaction Activity in your account', message_body, 'akshattesting@gmail.com', [user_data[0]['email']])
            mail.send()

        return Response('Your final amount now is: '+ str(balance_amount))

        # {"email":"goelakshat005@gmail.com",
        # "type_of_transaction":"Deposit",
        # "amount_changed":4000,
        # "password":"12345"}

@api_view(['GET','POST','PUT'])
def enquiry_download(request):
    if request.method == 'GET':

        return Response('Welcome to the Bank!')

    elif request.method == 'POST':           # To enquire about transactions
        user_data = User.objects.filter(email=request.data['email']).values()
        user_data_object = User.objects.filter(email=request.data['email'])
        
        start_date = '2000-01-01' + ' 00:00:00'
        end_date = datetime.datetime.combine(datetime.date.today(), datetime.time.max) 
        # print(end_date)

        if request.data['start_date'] != "None":
            start_date = request.data['start_date'] + ' 00:00:00'
        if request.data['end_date'] != "None":
            end_date = request.data['end_date'] + ' 11:59:59'
        # print(start_date,end_date)
        transaction_data = Transactions.objects.filter(email = user_data_object[0]).filter(date_transaction__range = (start_date,end_date)).values('date_transaction', 'amount_changed','type_of_transaction','final_amount')

        to_return_dict = {}
        if request.data['password'] == user_data[0]['password']:
            to_return_dict['Name of Account Holder'] = user_data[0]['name']
            to_return_dict['Date of Creation of Account'] = user_data[0]['creation_date']
            to_return_dict['Balance amount in account'] = user_data[0]['balance_amount']
            to_return_dict['transaction_data'] = transaction_data

        return Response(to_return_dict)

        # {"email":"goelakshat005@gmail.com",
        # "password":"12345",
        # "start_date":"2021-01-26",
        # "end_date":"None"}

    elif request.method == 'PUT':  # for managerial purpose 
        # since automatically a manager record is created in the earlier function so we need only specify the operations with right password
        start_date = '2000-01-01' + ' 00:00:00'
        end_date = datetime.datetime.combine(datetime.date.today(), datetime.time.max) 

        if request.data['start_date'] != "None":
            start_date = request.data['start_date'] + ' 00:00:00'
        if request.data['end_date'] != "None":
            end_date = request.data['end_date'] + ' 11:59:59'
        
        all_users = User.objects.filter(email__in=eval(request.data['all_emails']))
        all_data = []
        for user in all_users:
            name_email = User.objects.filter(id=user.id).values()
            data = Transactions.objects.filter(email = user).filter(date_transaction__range = (start_date,end_date)).values('date_transaction', 'amount_changed','type_of_transaction','final_amount')
            for ele in data:
                ele['Name'] = name_email[0]['name']
                ele['Email'] = name_email[0]['email']
            all_data += data
        
        print(all_data)
        df = pd.DataFrame(all_data)
        df['date_transaction'] = df['date_transaction'].apply(lambda a: pd.to_datetime(a).date())
        writer = pd.ExcelWriter('User_data.xlsx')
        df.to_excel(writer,'Sheet1')
        writer.save()

        return Response('User Data Downloaded!')

        # {"start_date":"None",
        # "end_date":"None",
        # "all_emails":"['goelakshat005@gmail.com','ayug99@gmail.com','gaurav.mait.gupta@gmail.com']",
        # "password":"manager@123"}