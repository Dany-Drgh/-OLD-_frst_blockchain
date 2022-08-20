import hashlib
import json

from time import time
from uuid import uuid4

from flask import flask

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(proof= 100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
        # Create a new Block in the Blockchain
        # proof: <int> The proof given by the Proof of Work algorithm
        # previous_hash: (Optional) <str> Hash of previous Block
        # return: <dict> New Block

        block = {
            "index": len(self.chain)+1,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }

        # Resetting current transaction lists
        self.current_transactions = []
        return block
        

    def new_transaction(self, sender, recipient, amount ):
        # Creates a new transaction to go into the next mined Block
        # :return: <int> The index of the Block that will hold this transaction
        self.current_transactions.append({
            'sender': sender,
            'recipient' : recipient,
            'amount' : amount
        } )

        return self.last_block['index']+1

    def proof_of_work(self, last_proof):
        # Simple Proof of Work Algorithm:
        #  - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        #  - p is the previous proof, and p' is the new proof

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        # Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'


    @staticmethod 
    def hash(block):
        # Hashes a Block with SHA-256
        # Dictionary has to be Ordered or  have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns last Block of the blockchain
        return self.chain[-1]

