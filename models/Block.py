from flask_sqlalchemy import SQLAlchemy
from ..app import db

#class for blocks
class Blocks(db.Model):
    __tablename__ = 'Blocks'

    block_hash = db.Column(db.String,primary_key=True)
    previous_block_hash = db.Column(db.String,ForeignKey='blocks.block_hash')
    timestamp = db.Column(db.Integer)
    block_height = db.Column(db.Integer)