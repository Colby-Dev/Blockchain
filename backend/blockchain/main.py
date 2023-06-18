import pytest

from backend.blockchain.Block import Block

class Blockchain:
    '''
    The blockchain is a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    '''

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        '''
        Replace the local chain with the incoming one if the following is met:
        - Incoming chain is longer than the local one
        - Incoming chain is formatted properly
        '''

        if len(chain) <= len(self.chain):
            raise Exception("Can't replace chain, new chain is not longer than current chain.")
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid because: {e}')

        self.chain = chain


    def to_json(self):
        '''
        Serialize the blockchain into a list of blocks
        '''
        serialized_chain = [block.to_json() for block in self.chain]
        return serialized_chain

    @staticmethod
    def is_valid_chain(chain):
        '''
        Validate the incoming chain
        It should enforce the rules of the Blockchain:
        -The chain must start with the genesis block
        -Blocks must be formatted correctly
        '''

        if chain[0].__dict__ != Block.genesis().__dict__:
            raise Exception('The genesis block needs to be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)




def main():
    blockchain = Blockchain()
    # blockchain.add_block('one')
    # blockchain.add_block('two')


    print(__name__)
    print(blockchain)

if __name__ == '__main__':
    main()