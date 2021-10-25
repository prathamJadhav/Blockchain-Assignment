import app
import merkleTree
import random


class Node:
    #this method id the validate method for every single node in the blockchain
    def validate(self, forger_previous_block_hash, forger_merkle_root):
        # every node checks the transactions from the unverified table
        unverifiedTransactions = app.Unverified_Transactions.query.order_by(
            app.Unverified_Transactions.timestamp).all()

        # every node gets the last block created block to check previous block hash value
        block = app.Blocks.query.order_by(
            app.Blocks.timestamp.desc()).first()  # gets last block created
        blockHeight = app.Blocks.query.count()
        previous_block_hash = None

        count = 0

        # creating list for calculating merkle root
        listForMerkle = []
        for unverified in unverifiedTransactions:
            if(count < 10):
                # making the merke tree
                listForMerkle.append(
                    unverified.tid+unverified.customer + str(unverified.amount)+str(unverified.timestamp))
                count += 1
            else:
                break

        # merkle root according to validator
        merkleRoot = (merkleTree.buildTree(listForMerkle))

        if block is None:
            previous_block_hash = None
        else:
            blockHeight = blockHeight
            previous_block_hash = block.block_hash

        # every validator node will check for he correctness of the block
        accepted = 0  # accepted = 0 -> rejected ; accpeted =1 ->accpeted

        # to display byzantine behaviour we have added randomness
        # according to this a node will exhibit byzantine behaviour with 1/15 probability
        random1 = random.randint(1, 15)
        random2 = random.randint(1, 15)
        print("random1 : ", random1)
        print("random2 : ", random2)

        # this is just to display byzantine behaviour
        # byzantine behaviour means if node know block should be accepted it will reject it and vice versa
        byzantine = False
        if random1 == random2:
            byzantine = True
        if merkleRoot == forger_merkle_root and previous_block_hash == forger_previous_block_hash:
            if byzantine == False:
                accepted = 1
        else:
            if byzantine == True:
                accepted = 1

        print("accepted : ", accepted)

        return accepted
