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
from ProofOfStake import POS
import random
import node

app = Flask(__name__, static_folder='frontend/build/static',
            template_folder='frontend/build')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eqcarzlf:OPWaAQ7FGpVc1uLXBrpZBfEDd_QbRphZ@chunee.db.elephantsql.com/eqcarzlf'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://znbormsc:7bHI6eqE45hLX4PT0Wj5Ll3BlktVshxR@arjuna.db.elephantsql.com/znbormsc'

db = SQLAlchemy(app)
db.init_app(app)
# app.debug(True)
CORS(app, support_credentials=True)
# pos = POS()
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

# table for nodes to store the nodes along with stake
class Nodes(db.Model):
    node_id = db.Column(db.String, primary_key=True)
    node_name = db.Column(db.String)
    stake = db.Column(db.Float)
    timestamp = db.Column(db.Integer)

    def __init__(self, node_id, node_name, stake, timestamp):
        self.node_id = node_id
        self.node_name = node_name
        self.stake = stake
        self.timestamp = timestamp

# table for stake updates to track changes in stake of node
class StakeUpdates(db.Model):
    stakeUpdateId = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String, db.ForeignKey('nodes.node_id'))
    block_hash = db.Column(db.String(256))
    initialStake = db.Column(db.Float)
    finalStake = db.Column(db.Float)
    timestamp = db.Column(db.Integer)

    def __init__(self, node_id, block_hash, initialStake, finalStake, timestamp):
        self.node_id = node_id
        self.block_hash = block_hash  # NULL in case of failed transaction
        self.initialStake = initialStake
        self.finalStake = finalStake
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

# adding a node into the Node table
@app.route('/api/addNode', methods=['POST'])
def newNode():
    json_data = request.get_json()

    node_name = json_data['node_name']  # name
    stake = json_data['stake']  # stake
    node_id = json_data['node_id']  # unique node_id
    message = bytes(json_data['message'], 'utf-8')  # stringified json
    signature = json_data['signature']  # signature
    timestamp = int(round(time.time()))

    # checking authenticity of node adding authority i.e. Dexter
    key = RSA.import_key(open('public.pem').read())

    h = SHA256.new(message)

    try:
        pkcs1_15.new(key).verify(h, bytearray(base64.b64decode(signature)))
        response = {
            'message': 'Success',
            'error': False
        }

        node = Nodes(node_id, node_name, stake, timestamp)

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

# endpoint for adding unverified transaction
@app.route('/api/addTransaction', methods=['POST'])
def transaction():
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

# endpoint to view list of blocks
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

# endpoint to view list of registered nodes
@app.route('/api/viewNodes', methods=['GET'])
def viewNodes():
    nodesList = Nodes.query.order_by(Nodes.timestamp).all()

    response = []
    for node in nodesList:
        temp = {}
        temp['node_id'] = node.node_id
        temp['node_name'] = node.node_name
        temp['stake'] = node.stake
        temp['timestamp'] = node.timestamp

        response.append(temp)

    return jsonify(response), 200

# endpoint to view a particular nodes stake updates
@app.route('/api/viewStakeUpdates', methods=['POST'])
def viewStakeUpdates():

    json_data = request.get_json()

    node = json_data['node_id']
    updateList = StakeUpdates.query.filter_by(
        node_id=node).order_by(StakeUpdates.timestamp).all()

    response = []
    for update in updateList:
        temp = {}
        temp['node_id'] = update.node_id
        temp['block_hash'] = update.block_hash
        temp['initialStake'] = update.initialStake
        temp['finalStake'] = update.finalStake
        temp['timestamp'] = update.timestamp

        response.append(temp)

    return jsonify(response), 200

# endpoint to view verified transactions
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

# endpoint to view list of unverified transactions
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

# retruns list of nodes apart from forger node which act as validators/attesters
def getValidators(forger_id):
    # get the list of nodes which act as validator
    validatorList = []
    nodes = Nodes.query.all()
    for node in nodes:
        if node.node_id != forger_id:
            validatorList.append(node.node_id)
    return validatorList

# method which will check consensus of the validators/attestors
def validate(forger_id, forger_previous_block_hash, forger_merkle_root, transactionAmount, blockHash):
    validatorList = getValidators(forger_id)

    acceptingNodes = 0
    rejectingNodes = 0

    rejectingNodeList = []
    acceptingNodeList = []

    for validator in validatorList:
        # every validator node will check for he correctness of the block
        newNode = node.Node()
        accepted = newNode.validate(forger_previous_block_hash, forger_merkle_root)
        if accepted == 1:
            acceptingNodeList.append(validator)
            acceptingNodes += 1
        else:
            rejectingNodeList.append(validator)
            rejectingNodes += 1

    totalValidators = acceptingNodes + rejectingNodes
    consensus = acceptingNodes/totalValidators
    print("consensus : ", consensus)

    #checking if 2/3 majority has been acheived
    if consensus >= (2/3):
        print("consensus granted")
        distributeRewards(acceptingNodeList, rejectingNodeList,
                          accepted, forger_id, transactionAmount, blockHash)
        return True

    print("not granted")
    distributeRewards(acceptingNodeList, rejectingNodeList,
                      accepted, forger_id, transactionAmount, blockHash)
    return False

# method which distributes rewards and penalties according to the status of the validation method
def distributeRewards(acceptingNodeList, rejectingNodeList, accepted, forger_id, transactionAmount, block_hash):

    # transaction fee has been set 0.1% of the total transaction amount of all the transactions in the block
    reward = 0.001*transactionAmount / (len(acceptingNodeList) + len(rejectingNodeList) + 1)
    timestamp = int(round(time.time()))
    if accepted == 1:
        print("accepted")
        for node in acceptingNodeList:
            # get stake and update with reward
            nodeToBeUpdated = Nodes.query.filter_by(node_id=node).first()
            stake = nodeToBeUpdated.stake
            newStake = stake + reward
            stakeUpdate = StakeUpdates(node, block_hash, stake, newStake, timestamp)
            db.session.add(stakeUpdate)
            nodeToBeUpdated.stake = newStake
            db.session.commit()

        # for forger
        nodeToBeUpdated = Nodes.query.filter_by(node_id=forger_id).first()
        stake = nodeToBeUpdated.stake
        newStake = stake + reward
        stakeUpdate = StakeUpdates(
            forger_id, block_hash, stake, newStake, timestamp)
        db.session.add(stakeUpdate)
        nodeToBeUpdated.stake = newStake
        db.session.commit()

        # get stake and reduce because they rejected
        for node in rejectingNodeList:
            nodeToBeUpdated = Nodes.query.filter_by(node_id=node).first()
            stake = nodeToBeUpdated.stake
            newStake = stake - reward
            stakeUpdate = StakeUpdates(
                node, block_hash, stake, newStake, timestamp)
            db.session.add(stakeUpdate)
            nodeToBeUpdated.stake = newStake
            db.session.commit()

    else:
        print("rejected")
        for node in acceptingNodeList:
            # get stake
            nodeToBeUpdated = Nodes.query.filter_by(node_id=node).first()
            stake = nodeToBeUpdated.stake
            newStake = stake - reward
            stakeUpdate = StakeUpdates(
                node, block_hash, stake, newStake, timestamp)
            db.session.add(stakeUpdate)
            nodeToBeUpdated.stake = newStake
            db.session.commit()

        # for forger
        nodeToBeUpdated = Nodes.query.filter_by(node_id=forger_id).first()
        stake = nodeToBeUpdated.stake
        newStake = stake - reward
        stakeUpdate = StakeUpdates(
            forger_id, block_hash, stake, newStake, timestamp)
        db.session.add(stakeUpdate)
        nodeToBeUpdated.stake = newStake
        db.session.commit()

        for node in rejectingNodeList:
            nodeToBeUpdated = Nodes.query.filter_by(node_id=node).first()
            stake = nodeToBeUpdated.stake
            newStake = stake + reward
            stakeUpdate = StakeUpdates(
                node, block_hash, stake, newStake, timestamp)
            db.session.add(stakeUpdate)
            nodeToBeUpdated.stake = newStake
            db.session.commit()

    return

# endpoint which first decides forger and then makes block and passes to validators for validation
@app.route('/api/verifyTransaction', methods=['GET'])
def verify():
    # run the algorithm for pos and select a node
    nodesList = Nodes.query.all()
    pos = POS(nodesList)
    # send the transactions to the node
    # get the block from the selected node and send the block, traensctions to other nodes to verfiy

    unverifiedTransactions = Unverified_Transactions.query.order_by(
        Unverified_Transactions.timestamp).all()
    unverifiedCount = Unverified_Transactions.query.count()
    if unverifiedCount == 0:
        # if there are no transactions to verify simply return
        return jsonify({'message': 'empty'}), 200

    block = Blocks.query.order_by(
        Blocks.timestamp.desc()).first()  # gets the last block created
    blockHeight = Blocks.query.count()
    previous_block_hash = None
    hashString = ""

    count = 0
    transactionAmount = 0
    # making the list for calculating merkle root
    listForMerkle = []
    for unverified in unverifiedTransactions:
        if(count < 10):
            # making the merke tree
            listForMerkle.append(unverified.tid+unverified.customer +
                                 str(unverified.amount)+str(unverified.timestamp))
            transactionAmount += unverified.amount
            count += 1
        else:
            break

    if block is None:
        previous_block_hash = None
    else:
        previous_block_hash = block.block_hash

    # adding the transaction fee transaction
    # unverifiedTransactions.append(Unverified_Transactions(previous_block_hash,"Forger/Validator Fee",transactionAmount*0.05*-1,unverifiedTransactions[-1].timestamp))
    # unverified = unverifiedTransactions[-1]
    # listForMerkle.append(unverified.tid+unverified.customer + str(unverified.amount)+str(unverified.timestamp))

    # this decodes the forger node and it returns the node_id of the forger node
    forger = pos.forger(previous_block_hash)
    print("forger", forger)

    # the forger calculates merkle root
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

    hashString += merkleRoot
    blockHash = sha256(hashString.encode()).hexdigest()

    # this call here calls the validators to check correctness of newly created block
    validation = validate(forger, previous_block_hash,
                          merkleRoot, transactionAmount, blockHash)

    response = {}

    # if validators have reached 2/3 consenus
    if validation == True:
        # making new block
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

        response['message'] = "success"
        response['error'] = False
        return jsonify(response), 200

    else:
        response['message'] = "failure"
        response['error'] = True
        return jsonify(response), 400

# endpoint for verifying the blocks in the blockchain
@app.route('/api/verifyBlocks', methods=['GET'])
def verifyBlocks():
    # calculate the block hash again and then check if it matches the hash value
    blockList = Blocks.query.order_by(Blocks.timestamp).all()

    for block in blockList:

        hashString = ""

        if block.block_height == 0:
            hashString += str(block.timestamp) + str(block.block_height)
        else:
            hashString += str(block.timestamp) + block.previous_block_hash+str(block.block_height)

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
