from flask import Flask, jsonify
from markupsafe import escape
from backend.blockchain.main import Blockchain


blockchain = Blockchain()

app = Flask(__name__)

@app.route('/')
def route_default():
    return '<h1>Welcome</h1>'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    trans_data = 'transaction_data'
    blockchain.add_block(trans_data)
    return jsonify(blockchain.chain[-1].to_json())

app.run(port=5001)