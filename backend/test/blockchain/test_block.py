from backend.blockchain.Block import Block
from backend.blockchain.Block import GENESIS_DATA
import time
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary
import pytest

def test_mine_block():
    last_block = Block.genesis()
    data = 'last block data'
    block = Block.mine_block(last_block, data)
    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty


def test_genesis():
    test_gen_block = Block.genesis()
    assert isinstance(test_gen_block, Block)
    assert test_gen_block.timestamp == GENESIS_DATA['timestamp']
    assert test_gen_block.data == GENESIS_DATA['data']
    assert test_gen_block.hash == GENESIS_DATA['hash']
    assert test_gen_block.last_hash == GENESIS_DATA['last_hash']


def test_quickly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'testing')
    mine_block = Block.mine_block(last_block, 'block_diff_fast')

    assert mine_block.difficulty == last_block.difficulty + 1


def test_slowly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'testing')
    ##Time.sleep() converts inputs to seconds technically MINE_RATE = 4Billion nano so divide by 1Billion nano (SECONDS)
    time.sleep(MINE_RATE / SECONDS)
    mine_block = Block.mine_block(last_block, 'block_diff_slow')
    assert mine_block.difficulty == last_block.difficulty - 1
    '''
    This test below does not work. The keys for the GENISIS_DATA are different from the Block class. 
    In order to fix this change the keys in the genisis data hash table
    '''
    # for key, value in GENISIS_DATA.items():
    #     assert getattr(test_gen_block, key) == value


def test_mine_block_difficulty_at_1():
    last_block = Block(
        'test_data',
        time.time_ns(),
        'test_last_hash',
        'test_hash',
        1,
        0
    )

    time.sleep(MINE_RATE / SECONDS)

    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1

@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'testing data')

def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)

def test_is_valid_block_last_hash(last_block, block):
    block.last_hash = 'bad last hash'

    with pytest.raises(Exception, match='The block hash must match the previous hash!'):
        Block.is_valid_block(last_block, block)

def test_bad_proof_of_work(last_block, block):
    block.hash = 'eeee'

    with pytest.raises(Exception, match='The block hash does not have the required amount of leading 0s!'):
        Block.is_valid_block(last_block, block)

def test_bad_difficulty_setting(last_block, block):
    block.difficulty = 5
    block.hash=f'{"0" * 5}12aef33'
    with pytest.raises(Exception, match='The block difficulty must raise by only 1!'):
        Block.is_valid_block(last_block, block)

def test_valid_hash(last_block, block):
    block.hash = '0000000ea1233fefad'
    with pytest.raises(Exception, match='The block hash must be correct. Data is not accurate.'):
        Block.is_valid_block(last_block, block)
