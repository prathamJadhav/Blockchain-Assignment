from flask_sqlalchemy import SQLAlchemy
import os
from ..app import db
import datetime

#class for unverifired transactions
class Unverified_Transactions(db.Model):
    __tablename__ = 'Unverified_Transactions'

    tid = db.Column(db.Integer,primary_key=True)
    customer = db.Column(db.String)
    amount = db.Column(db.Float)
    timestamp = db.Column(db.Integer)

    def __init__(self,tid,customer,amount,**kwargs):
        super(Unverified_Transactions, self).__init__(**kwargs)
        self.tid = tid
        self.amount = amount
        self.customer = customer
        self.timestamp = datetime.datetime.now()