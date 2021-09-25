from flask_sqlalchemy import SQLAlchemy
from ..app import db

#class for verified transactions
class Verified_Transactions(db.Model):
    __tablename__ = 'Verified_Transactions'

    tid = db.Column(db.Integer,primary_key=True)
    customer = db.Column(db.String)
    amount = db.Column(db.Float)
    timestamp = db.Column(db.String)
    block_hash = db.Column(db.String,ForeignKey='blocks.block_hash')