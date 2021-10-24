from flask import Flask, json, request, jsonify, render_template
from flask.signals import message_flashed
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import time
from flask_cors import CORS, cross_origin
from hashlib import sha256
from Crypto import Signature
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64
import merkleTree
from ProofOfStake import ProofOfStake

app = Flask(__name__, static_folder='frontend/build/static',
            template_folder='frontend/build')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eqcarzlf:OPWaAQ7FGpVc1uLXBrpZBfEDd_QbRphZ@chunee.db.elephantsql.com/eqcarzlf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://znbormsc:7bHI6eqE45hLX4PT0Wj5Ll3BlktVshxR@arjuna.db.elephantsql.com/znbormsc'

db = SQLAlchemy(app)
db.init_app(app)
# app.debug(True)
CORS(app, support_credentials=True)
pos = ProofOfStake()
# app.config['CORS_HEADERS'] = 'Content-Type'

#api = Api(app,prefix='/api')

# api.add_resource(AddTransaction,'/addTransaction')


@app.route("/")
def hello():
    return render_template('index.html')


# class for blocks
class Blocks(db.Model):
    #__tablename__ = 'Blocks'

    block_hash = db.Column(db.String(256), primary_key=True)
    previous_block_hash = db.Column(
        (db.String(256)), db.ForeignKey('blocks.block_hash'))
    timestamp = db.Column(db.Integer)
    block_height = db.Column(db.Integer)
    merkleRoot = db.Column(db.String(256))

    def __init__(self, timestamp, block_hash, previous_block_hash, block_height, merkleRoot):
        self.block_hash = block_hash
        self.block_height = block_height
        self.previous_block_hash = previous_block_hash
        self.timestamp = timestamp
        self.merkleRoot = merkleRoot


class Nodes(db.Model):
    node_id = db.Column(db.Integer, primary_key=True)
    stake = db.Column(db.Numeric)
    timestamp = db.Column(db.Integer)

    def __init__(self, node_id, stake, timestamp):
        self.node_id = node_id
        self.stake = stake
        self.timestamp = timestamp

# class for verified transactions


class Verified_Transactions(db.Model):
    #__tablename__ = 'VerifiedTransactions'

    tid = db.Column(db.String, primary_key=True)
    customer = db.Column(db.String(256))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.String(256))
    block_hash = db.Column(db.String(256), db.ForeignKey('blocks.block_hash'))

    def __init__(self, tid, customer, amount, timestamp, block_hash):
        self.tid = tid
        self.amount = amount
        self.customer = customer
        self.timestamp = timestamp
        self.block_hash = block_hash


# #class for unverifired transactions
class Unverified_Transactions(db.Model):
    #__tablename__ = 'UnverifiedTransactions'

    tid = db.Column(db.String, primary_key=True)
    customer = db.Column(db.String(256))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.Integer)
    # unique_key = db.Column(db.)

    def __init__(self, tid, customer, amount, timestamp, **kwargs):
        super(Unverified_Transactions, self).__init__(**kwargs)
        self.tid = tid
        self.amount = amount
        self.customer = customer
        self.timestamp = timestamp
        #self.timestamp = int(round(dt.timestamp() * 1000))


with app.app_context():
    # your code here
    db.create_all()
    db.session.commit()


class Blockchain():
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = "-".join(transaction_list) + \
            "-" + previous_block_hash

        self.block_hash = sha256(self.block_data.encode()).hexdigest()

#adding a node into the Node table
@app.route('/api/addNode', methods=['POST'])
def transaction():
    json_data = request.get_json()

    node_name = json_data['node_name']  # name
    stake = json_data['stake']  # stake
    node_id = json_data['node_id']  # unique node_id
    message = bytes(json_data['message'], 'utf-8')  # stringified json
    signature = json_data['signature']  # signature
    timestamp = int(round(time.time()))
    #block_hash = json_data['block_hash']
    error = False

    # checking authenticity
    key = RSA.import_key(open('public.pem').read())

    h = SHA256.new(message)

    try:
        pkcs1_15.new(key).verify(h, bytearray(base64.b64decode(signature)))
        response = {
            'message': 'Success',
            'error': False
        }

        node = Nodes(node_id ,stake, timestamp)

        db.session.add(node)
        db.session.commit()

        return jsonify(response), 200  # 200-good, 400-bad
    except (ValueError, TypeError):
        response = {
            'message': 'Signature Invalid',
            'error': True
        }
        return jsonify(response), 400  # 200-good, 400-bad
    except (BaseException):
        response = {
            'message': 'Fraudulent Node',
            'error': True
        }
        return jsonify(response), 400  # 200-good, 400-bad


@app.route('/api/addTransaction', methods=['POST'])
def transaction():
    print('here')
    json_data = request.get_json()

    customer = json_data['customer']  # name
    amount = json_data['amount']  # amount
    tid = json_data['tid']  # unique tid
    message = bytes(json_data['message'], 'utf-8')  # stringified json
    signature = json_data['signature']  # signature
    timestamp = int(round(time.time()))
    #block_hash = json_data['block_hash']
    error = False

    # checking authenticity
    key = RSA.import_key(open('public.pem').read())

    h = SHA256.new(message)

    try:
        pkcs1_15.new(key).verify(h, bytearray(base64.b64decode(signature)))
        response = {
            'message': 'Success',
            'error': False
        }

        transaction = Unverified_Transactions(tid, customer, amount, timestamp)

        db.session.add(transaction)
        db.session.commit()

        return jsonify(response), 200  # 200-good, 400-bad
    except (ValueError, TypeError):
        response = {
            'message': 'Signature Invalid',
            'error': True
        }
        return jsonify(response), 400  # 200-good, 400-bad
    except (BaseException):
        response = {
            'message': 'Fraudulent Transaction',
            'error': True
        }
        return jsonify(response), 400  # 200-good, 400-bad


@app.route('/api/viewBlocks', methods=['GET'])
def viewBlocks():
    blocksList = Blocks.query.order_by(Blocks.timestamp).all()

    response = []
    for block in blocksList:
        temp = {}
        temp['block_hash'] = block.block_hash
        temp['previous_block_hash'] = block.previous_block_hash
        temp['timestamp'] = block.timestamp
        temp['block_height'] = block.block_height
        temp['merkleRoot'] = block.merkleRoot

        response.append(temp)

    return jsonify(response), 200


@app.route('/api/viewTransactions', methods=['POST'])
def viewTransactions():
    json_data = request.get_json()
    blockHash = json_data['block_hash']

    transactionsList = Verified_Transactions.query.filter_by(
        block_hash=blockHash).order_by(Verified_Transactions.timestamp).all()

    response = []
    for transaction in transactionsList:
        temp = {}
        temp['tid'] = transaction.tid
        temp['block_hash'] = transaction.block_hash
        temp['customer'] = transaction.customer
        temp['amount'] = transaction.amount
        temp['timestamp'] = transaction.timestamp

        response.append(temp)

    return jsonify(response), 200


@app.route('/api/viewUnverifiedTransactions', methods=['GET'])
def viewUnverifiedTransactions():

    transactionsList = Unverified_Transactions.query.order_by(
        Unverified_Transactions.timestamp).all()

    response = []
    for transaction in transactionsList:
        temp = {}
        temp['tid'] = transaction.tid
        temp['block_hash'] = transaction.block_hash
        temp['customer'] = transaction.customer
        temp['amount'] = transaction.amount
        temp['timestamp'] = transaction.timestamp

        response.append(temp)

    return jsonify(response), 200


@app.route('/api/verifyTransaction', methods=['GET'])
def verify():
    # query and get the list of unverified transactions sorted according to ascending timestamps

    # run the algorithm for pos and select a node
    # get nodes from sql
    nodesList = Nodes.query.order_by(Nodes.node_id).all()
    print(nodesList[0].node_id)
    # send the transactions to the node
    # get the block from the selected node and send the block, traensctions to other nodes to verfiy

    unverifiedTransactions = Unverified_Transactions.query.order_by(
        Unverified_Transactions.timestamp).all()
    unverifiedCount = Unverified_Transactions.query.count()
    if unverifiedCount == 0:
        # if there are no transactions to verify simply return

        return jsonify({'message': 'empty'}), 200

    block = Blocks.query.order_by(
        Blocks.timestamp.desc()).first()  # gets all the blocks
    blockHeight = Blocks.query.count()
    previous_block_hash = None
    hashString = ""

    count = 0
    # making the unverified transaction into verified transaction
    listForMerkle = []
    for unverified in unverifiedTransactions:
        if(count < 10):
            # making the merke tree
            listForMerkle.append(unverified.tid+unverified.customer +
                                 str(unverified.amount)+str(unverified.timestamp))

            count += 1

        else:
            break

    merkleRoot = (merkleTree.buildTree(listForMerkle))

    timestamp = int(round(time.time()))

    if block is None:
        # make genessis block
        blockHeight = 0
        previous_block_hash = None

        hashString += str(timestamp) + str(blockHeight)

    else:
        blockHeight = blockHeight
        previous_block_hash = block.block_hash

        # make a new block and previous block hash is block hash of bloxk
        response = {'message': 'success'}
        hashString = ""

        hashString += str(timestamp) + previous_block_hash + str(blockHeight)

    response = {'message': 'success'}
  #forger --------------
    
    forger = pos.forger(previous_block_hash)




    # this represents the block hash
    hashString += merkleRoot

    blockHash = sha256(hashString.encode()).hexdigest()

    newBlock = Blocks(timestamp, blockHash,
                      previous_block_hash, blockHeight, merkleRoot)

    db.session.add(newBlock)
    db.session.commit()

    count = 0
    # making the unverified transaction into verified transaction
    for unverified in unverifiedTransactions:
        if(count < 10):
            # making the verified entry
            verified = Verified_Transactions(
                unverified.tid, unverified.customer, unverified.amount, unverified.timestamp, blockHash)

            # removing the transaction from unverified table
            db.session.delete(unverified)

            # adding into verified table
            db.session.add(verified)
            db.session.commit()
            count += 1

        else:
            break

    return jsonify(response), 200


@app.route('/api/verifyBlocks', methods=['GET'])
def verifyBlocks():
    # calculate the block hash again and then check if it matches the hash value
    blockList = Blocks.query.order_by(Blocks.timestamp).all()

    for block in blockList:

        hashString = ""

        if block.block_height == 0:
            hashString += str(block.timestamp) + str(block.block_height)
        else:
            hashString += str(block.timestamp) + \
                block.previous_block_hash+str(block.block_height)

        transactionList = Verified_Transactions.query.filter_by(
            block_hash=block.block_hash).all()
        # print(str(Verified_Transactions.query.filter_by(block_hash=block.block_hash).count()))

        # get the transactions and make the merkle root
        listForMerkle = []
        for transaction in transactionList:
            # making the merke tree
            listForMerkle.append(transaction.tid+transaction.customer +
                                 str(transaction.amount)+str(transaction.timestamp))

        merkleRoot = (merkleTree.buildTree(listForMerkle))

        hashString += merkleRoot

        checkHash = sha256(hashString.encode()).hexdigest()

        message = ""

        response = {}

        #print(block.block_hash + " -- " + checkHash + "--" + str(block.block_height))

        if checkHash != block.block_hash:
            message = 'Error'
            response['message'] = message
            response['error'] = True
            return jsonify(response), 400

    message = 'success'
    response['message'] = message
    response['error'] = False
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', use_reloader=True, port=9000, debug=True)
