# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 13:47:59 2019

@author: jackd
"""

import datetime
import json
import hashlib
from flask import Flask, jsonify
import requests
from uuid import uuid4
from urllib.parse import urlparse


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions[]
        self.create_block(proof=1, previous_hash=0)
        self.nodes{}

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
            'transactions':  self.transactions
        }
        self.transactions.clear()
        self.chain.append(block)
        return block
    
    
    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
        
    def replace_chain(self):
        network= self.nodes
        longest_chain  = None
        max_length = len(self.chain)
   for node in network:
       response = requests.get(f'http://{node}/get_chain')
       if response.status_code ==200:
           length = response.json()['length']
           chain = response.json()['chain']
           if length > max_length and self.is_chain_valid(chain):
              max_length = length
              longest_chain = chain
       if longest_chain:
            self.chain= longest_chain
            return True
        return False
    
    
    def add_transaction(self,sender,receiever,amount):
        self.transactions.append({'sender':sender,
                            'receiever':receiever,
                            'amount':amount))
        latest_block = self.get_previous_block()
        
        return latest_block['index']+1
    
    def get_previous_block(self):
        return self.chain[-1]
    
    

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while(check_proof is False):
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if(hash_operation[:4] == "0000"):
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_chain = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if(block['previous_hash'] != self.hash(previous_block)):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if(hash_operation[:4] != "0000"):
                return False
            previous_block = block
            block_index += 1
        return True


app = Flask(__name__)

blockchain = Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'New Bloc created',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof':  block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
            'chain':blockchain.chain,
            'length':len(blockchain.chain)
            }
    return jsonify(response),200
@app.route('/is_valid',methods=['GET'])
def is_valid():
    chain = blockchain.chain
    chainstatus = blockchain.is_chain_valid(cahin),
    if(cahinstatus is True):
        status = 'this chain is valid'
    else:
        status = 'this chain is not  valid'
    response = {
            'status': status
            }
    return jsonify(response),200
app.run(host='0.0.0.0',port=5000)