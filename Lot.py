from BlockchainUtils import BlockchainUtils


class Lot():
    def __init__(self, node_id, iteration, lastBlockHash):
        self.node_id = str(node_id)
        self.iteration = iteration
        self.lastBlockHash = str(lastBlockHash)

    def lotHash(self):
        hashData = self.node_id + self.lastBlockHash
        for _ in range(self.iteration):
            hashData = BlockchainUtils.hash(hashData).hexdigest()
        return hashData
