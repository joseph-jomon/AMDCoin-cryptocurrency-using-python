"""
Created on Wed Feb 20 10:49:09 2019

@author: Sumith
"""

import datetime
import json
import hashlib
from flask import Flask, jsonify

class Blockchain:
 # initialize variables and calling functions   
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
 # Create new block       
    def create_block(self,proof, previous_hash):
        block = {'index' : len(self.chain)+1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash}
        block['Hash'] = self.hash(block)
        self.chain.append(block)
        return block
    
# Get previous block        
    def get_previous_block(self):
        return self.chain[-1]
    
 # proof of work   
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            
            block_data = str(new_proof** 2-previous_proof** 2) # Nance equivalent
            hash_value = hashlib.sha256((block_data).encode()).hexdigest()
            
            if hash_value [:4] == "0000":
                check_proof = True
                return new_proof
            else:
                new_proof += 1
                
 # Finding hash               
    def hash (self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()             
        hash_value = hashlib.sha256(encoded_block).hexdigest()
        return hash_value
    
# Varification
        

    def is_valid_chain(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # varifying hashes of current and previous
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # varifying proofs of current and previous
            previous_proof = previous_block['proof']
            proof = block['proof']
            block_data = str(proof** 2-previous_proof** 2) # Nance equivalent
            hash_value = hashlib.sha256((block_data).encode()).hexdigest()
            if hash_value [:4] != "0000":
                return False
            # incrementing previous block by equating current block to previous block
            previous_block = block
            # incrementing current block 
            block_index += 1
        return True
    
#----------------------------------------------    
# mining
#----------------------------------------------
        
# Creating a web app
app = Flask(__name__)

# Create object

blockchain = Blockchain()

@app.route('/mine_block',methods = ['GET'])
def mine_block():
    
    previous_block = blockchain.get_previous_block ()
    
    # how to find proof
    
    previous_proof = previous_block['proof']
    
    proof = blockchain.proof_of_work(previous_proof)
    
    # how to find previous_hash
    
    previous_hash = blockchain.hash(previous_block)
    
    block = blockchain.create_block(proof, previous_hash)
    
    # Display contents of new block
    
    response = {'Message' : 'New block mined!',
                'index' : block['index'],
                'time stamp' : block['timestamp'],
                'proof' : block['proof'],
                'Hash' : blockchain.hash(block),
                'previous_hash' : block['previous_hash']}
    
    return jsonify(response),200 # 200 is status code for SUCCESS 
                                  # jsonify used to show data in POSTMAN
    
# Display chain
@app.route('/get_chain',methods = ['GET'])  
def get_chain():
    response = {'chain' : blockchain.chain,
                
                'length' : len(blockchain.chain),
                }
    
    return jsonify (response),200 # 200 is status code for SUCCESS 
                                  # jsonify used to show data in POSTMAN

#varify function in Postman
@app.route('/valid',methods = ['GET']) 
def valid():
    response = {'chain' : blockchain.chain,
                'Valid' : blockchain.is_valid_chain(blockchain.chain),
                'length' : len(blockchain.chain),
                }
    
    return jsonify (response),200 # 200 is status code for SUCCESS 
                                  # jsonify used to show data in POSTMAN
                                  
#running the app
app.run(host = '0.0.0.0',port = 5000)


                         