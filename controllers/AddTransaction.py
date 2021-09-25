from flask import json,request
from ..models import Unverified_Transactions
import time

class AddTransaction():
    #making the transaction

    def __init__(self):
        json_data = request.get_json()

        customer = json_data['customer']
        amount = json_data['amount']
        timestamp = int(round(time.time()))
        #block_hash = json_data['block_hash']

        #making the SQL query for inputting into unverified transactions
        transaction = Unverified_Transactions(customer,amount,timestamp)
    