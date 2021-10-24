from app import Unverified_Transactions, Blocks
import merkleTree
import random

class Node:
    def validate(self,forger_previous_block_hash, forger_merkle_root):
        unverifiedTransactions = Unverified_Transactions.query.order_by(Unverified_Transactions.timestamp).all()

        block = Blocks.query.order_by(Blocks.timestamp.desc()).first()  # gets all the blocks
        blockHeight = Blocks.query.count()
        previous_block_hash = None

        count = 0
        
        # creating list for calculating merkle root
        listForMerkle = []
        for unverified in unverifiedTransactions:
            if(count < 10):
                # making the merke tree
                listForMerkle.append(unverified.tid+unverified.customer + str(unverified.amount)+str(unverified.timestamp))
                count += 1
            else:
                break

        # the forger makes the block
        merkleRoot = (merkleTree.buildTree(listForMerkle))

        if block is None:
            previous_block_hash = None
        else:
            blockHeight = blockHeight
            previous_block_hash = block.block_hash

        #every validator node will check for he correctness of the block
        accepted = 0 #accepted = 0 -> rejected ; accpeted =1 ->accpeted
        random1 = random.randint(1,100)
        random2 = random.randint(1,100)
        print("random1 : ",random1)
        print("random2 : ",random2)
        byzantine = False
        if random1==random2:
            byzantine = True
        if merkleRoot == forger_merkle_root and previous_block_hash == forger_previous_block_hash:
            if byzantine == False:
                accepted=1
        else:
            if byzantine == True:
                accepted=1

        print("accepted : ",accepted)

        return accepted