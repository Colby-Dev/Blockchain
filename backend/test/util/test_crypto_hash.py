'''
This file test the blockchain hashing via an assert statement to ensure the hashes are the same based on the test case below.
'''

from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
    assert crypto_hash(1, [2], 'three') == crypto_hash('three', 1, [2])
    # assert crypto_hash('test') == '4d967a30111bf29f0eba01c448b375c1629b2fed01cdfcc3aed91f1b57d5dd5e'