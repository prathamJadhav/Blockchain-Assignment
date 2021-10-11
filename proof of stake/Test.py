from ProofOfStake import ProofOfStake
from Lot import Lot
import string
import random

#for getting seed (last Block hash) -->for testing purpose
def getRandomString(length):
    letters = string.ascii_lowercase
    resultString = ''.join(random.choice(letters) for i in range(length))
    return resultString


if __name__ == '__main__':
    pos = ProofOfStake()
    pos.update('node1', 10)
    pos.update('node2', 20)
    pos.update('node3', 30)
    pos.update('node4', 40)

    node1Stake =pos.get('node1');
    print('Node1 stake: ' + str(node1Stake))

    node2Stake =pos.get('node2');
    print('Node2 stake: ' + str(node2Stake))

    node3Stake =pos.get('node3');
    print('Node3 stake: ' + str(node3Stake))

    node4Stake =pos.get('node4');
    print('Node4 stake: ' + str(node4Stake))

    totalStakes =node1Stake+node2Stake+node3Stake+node4Stake;

    node1Won = 0
    node2Won = 0
    node3Won = 0
    node4Won = 0

   #testing on 100 scenarios

    for i in range(100):
        forger = pos.forger(getRandomString(i))
        if forger == 'node1':
            node1Won += 1
            node1Stake += (node1Stake/totalStakes);

        elif forger == 'node2':
            node2Won += 1
            node2Stake += (node2Stake/totalStakes);
        elif forger == 'node3':
            node3Won += 1
            node3Stake += (node3Stake/totalStakes);
        elif forger == 'node4':
            node4Won += 1
            node4Stake += (node4Stake/totalStakes);

    print('Node1 wins: ' + str(node1Won) + ' times')
    print('Node2 wins: ' + str(node2Won) + ' times')
    print('Node3 wins: ' + str(node3Won) + ' times')
    print('Node4 wins: ' + str(node4Won) + ' times')

    
    print('Node1 stake: ' + str(node1Stake))

    
    print('Node2 stake: ' + str(node2Stake))

    
    print('Node3 stake: ' + str(node3Stake))

   
    print('Node4 stake: ' + str(node4Stake))
