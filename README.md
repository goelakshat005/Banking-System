# Banking-System
Problem Statement:
A bank system which manages users’ account information. A customer of this bank can invoke the following operations
1. Deposit (this operation increases the balance of user account by a given amt)
2. Withdraw (this operation decreases the balance of user account by given amt)
3. Enquiry ( this operation returns the balance of user account etc)
4. Customer should receive emails on transactions
5. The bank manager should be able to download excel of transaction histories for a specific time period for individual/a collection of customers 


Solution:
Run requirements.txt file using command 'pip install -r requirements.txt'.

I have created two models namely 'User' and 'Transactions'. User model stores the information about the existing or a new user when created, along with balance amount in the user's account, and date of creation of amount as well.  Transactions model is for keeping a track of all the users activity including withdrawal and deposit amount along with the final amount after each transaction, and the date of transaction as well.

URLs:
http://127.0.0.1:8000/banking_system/creationupdation/
GET: It welcomes you to the bank and also if the manager record for password is not created then it is automatically created for the manager.

POST: A new user is created by giving the following details. An email is also sent to the newly created user.
{"name":"akshat goel",
 "email":"goelakshat005@gmail.com",
 "balance_amount":50000,
 "password":"12345"}

PUT: When an existing user has to make a transaction, whether withdrawal or deposit then he/she has to provide with the following details. Also an automated mail is sent to the the user's emailid to update him/her regrading the same.
{"email":"goelakshat005@gmail.com",
 "type_of_transaction":"Deposit",
 "amount_changed":4000,
 "password":"12345"}


http://127.0.0.1:8000/banking_system/enquirydownload/
POST: It gives the user all the details of his/her account and it's transaction by entering 'email' and 'password' along with the time frame 'startdate' and 'enddate'. If both start and end dates are none then it is assumed that user wants all the transactions and if any of them is provided then it considers it to be the limit.
{"email":"goelakshat005@gmail.com",
 "password":"12345",
 "start_date":"2021-01-26",
 "end_date":"None"}

PUT: It gives manager of the bank the option to download the user data depending upon the email ids and time frame he/she has provided. An excel sheet is created depending on the filters. Manager also has to provide the password personal to him/her for downloading the data.
{"start_date":"None",
 "end_date":"None",
 "all_emails":"['goelakshat005@gmail.com','ayug99@gmail.com','gaurav.mait.gupta@gmail.com']",
 "password":"manager@123"}
