import hashlib
import json
from time import time
from ecdsa import SigningKey, VerifyingKey, NIST384p

class Transaction:
    def __init__(self, sender_public_key, recipient_address, amount):
        self.sender_public_key = sender_public_key
        self.recipient_address = recipient_address
        self.amount = amount
        self.signature = None

    def to_dict(self):
        return {
            'sender': self.sender_public_key,
            'recipient': self.recipient_address,
            'amount': self.amount,
            'signature': self.signature
        }

    def sign_transaction(self, private_key):
        """
        Sign transaction with private key
        """
        sk = SigningKey.from_string(bytes.fromhex(private_key), curve=NIST384p)
        message = str(self.sender_public_key) + self.recipient_address + str(self.amount)
        self.signature = sk.sign(message.encode()).hex()

    def is_valid(self):
        """
        Verify transaction signature
        """
        if self.amount <= 0:
            return False
        if not self.signature:
            return False
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(self.sender_public_key), curve=NIST384p)
            message = str(self.sender_public_key) + self.recipient_address + str(self.amount)
            return vk.verify(bytes.fromhex(self.signature), message.encode())
        except:
            return False

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.difficulty = 2

    def create_genesis_block(self):
        genesis_block = Block(0, [], time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_transaction(self, transaction):
        if transaction.is_valid():
            self.unconfirmed_transactions.append(transaction)
            return True
        return False

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def mine_block(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.chain[-1]

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        new_block.hash = proof
        self.chain.append(new_block)
        self.unconfirmed_transactions = []
        return new_block.index

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.compute_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

            for tx in current.transactions:
                if not tx.is_valid():
                    return False

            if not current.hash.startswith('0' * self.difficulty):
                return False
        return True

def generate_key_pair():
    sk = SigningKey.generate(curve=NIST384p)
    vk = sk.get_verifying_key()
    return sk.to_string().hex(), vk.to_string().hex()

# Example usage
if __name__ == "__main__":
    # Create blockchain
    blockchain = Blockchain()

    # Generate key pairs
    private_key1, public_key1 = generate_key_pair()
    private_key2, public_key2 = generate_key_pair()

    # Create transaction
    transaction1 = Transaction(public_key1, public_key2, 5)
    transaction1.sign_transaction(private_key1)

    # Add transaction to blockchain
    blockchain.add_transaction(transaction1)

    # Mine block
    blockchain.mine_block()

    # Verify blockchain
    print("Blockchain valid:", blockchain.is_chain_valid())

    # Print blocks
    for block in blockchain.chain:
        print(f"Block {block.index}")
        print(f"Hash: {block.hash}")
        print(f"Previous hash: {block.previous_hash}")
        print("Transactions:")
        for tx in block.transactions:
            print(f"From: {tx.sender_public_key[:10]}...")
            print(f"To: {tx.recipient_address[:10]}...")
            print(f"Amount: {tx.amount}")
            print(f"Valid: {tx.is_valid()}")
        print("\n")