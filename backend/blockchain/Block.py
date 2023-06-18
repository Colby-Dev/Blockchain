import time
from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.util.hex_to_binary import hex_to_binary

'''
The Genesis data is primarily used for testing the genesis block. The difficulty correlates to the amount of zeroes
before the hash. The nonce is the iteration of the hash that was generated for the block. 

'''

GENESIS_DATA = {
    'data': 'genesis_data',
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    """
    a block is a unit of storage
    this will store transactions in a blockchain that supports a cryptocurrency.
    """

    def __init__(self, data, timestamp, last_hash, hash, difficulty, nonce):
        self.data = data
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            f' Block: ('
            f' Data: {self.data},'
            f' Timestamp: {self.timestamp},'
            f' Last Hash: {self.last_hash},'
            f' Hash: {self.hash},'
            f' Difficulty: {self.difficulty},'
            f' Nonce: {self.nonce})'
        )

    def to_json(self):
        '''
        Serialize the block into a dictionary
        '''
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        """
        Mines a block based on the given last_block and data
        :param last_block:
        :param data:
        :return: continuously mine a new block instance with the data given until
         a block hash is found with the correct number of leading zeroes
        """

        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = last_block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = last_block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(data, timestamp, last_hash, hash, difficulty, nonce)

    @staticmethod
    def genesis():
        """
        :return: Generate a genesis block.
        """

        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        '''

        :param last_block: the last block mined
        :param new_timestamp: the new timestamp for the mined block
        :return: an adjusted difficulty based off the mine rate, that increases or decreases
        '''

        if(new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
        if(last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1
        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        '''
        Validate a block by:
         -making sure the last block hash == current block hash
         -making sure the hash has the correct amount of leading zeroes that match the difficulty
         -making sure the difficulty only adjust by 1
         -making sure the block hash is a valid combination of the hash data
        '''

        if block.last_hash != last_block.hash:
            raise Exception('The block hash must match the previous hash!')
        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The block hash does not have the required amount of leading 0s!')
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must raise by only 1!')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
            # block.hash
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct. Data is not accurate.')




def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(Block.genesis(), 'test')
    # bad_block.last_hash = 'bad data'
    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')
    # block = Block.mine_block(genesis_block, 'one')
    # block2 = Block.mine_block(block, 'two')
    # block3 = Block.mine_block(block2, '3')
    # print(block)
    # print(block2)
    # print(block3)


if __name__ == '__main__':
    main()
