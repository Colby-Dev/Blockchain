import pytest

from backend.blockchain.main import Blockchain
from backend.blockchain.Block import GENESIS_DATA

def test_blockchain_instance():
    blockchain = Blockchain()
    assert(blockchain.chain[0].hash == GENESIS_DATA['hash'])

def test_add_block():
    blockchain = Blockchain()
    test_data = 'test-data'
    blockchain.add_block(data=test_data)
    assert(blockchain.chain[-1].data == test_data)

@pytest.fixture
def add_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block(i)
    return blockchain

def test_is_valid_chain(add_three_blocks):
    Blockchain.is_valid_chain(add_three_blocks.chain)

def test_is_valid_bad_genesis_block(add_three_blocks):
    add_three_blocks.chain[0].hash = 'hash'

    with pytest.raises(Exception, match='The genesis block needs to be valid'):
        Blockchain.is_valid_chain(add_three_blocks.chain)

def test_replace_chain(add_three_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(add_three_blocks.chain)

    assert blockchain.chain == add_three_blocks.chain

def test_replace_chain_short_chain(add_three_blocks):
    blockchain = Blockchain()

    with pytest.raises(Exception, match="Can't replace chain, new chain is not longer than current chain."):
        add_three_blocks.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain(add_three_blocks):
    blockchain = Blockchain()
    add_three_blocks.chain[0].hash = 'bad_hash'

    with pytest.raises(Exception, match="Cannot replace. The incoming chain is invalid because:"):
        blockchain.replace_chain(add_three_blocks.chain)