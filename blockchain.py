import hashlib
import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def update_data(self, new_data):
        self.data = new_data
        self.hash = self.calculate_hash()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            timestamp=datetime.datetime.now(),
            data=new_data,
            previous_hash=previous_block.hash,
        )
        self.chain.append(new_block)
        print("Block added successfully!")

    def display_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print("--------------")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid block at index {i}")
                return False
            if current_block.previous_hash != previous_block.hash:
                print(f"Broken chain at index {i}")
                return False
        return True

    def search_block(self, query):
        results = []
        for block in self.chain:
            if query in block.data:
                results.append(block)
        
        if results:
            print(f"Found {len(results)} block(s) containing '{query}':")
            for block in results:
                print(f"Index: {block.index}")
                print(f"Timestamp: {block.timestamp}")
                print(f"Data: {block.data}")
                print(f"Hash: {block.hash}")
                print(f"Previous Hash: {block.previous_hash}")
                print("--------------")
        else:
            print(f"No blocks found containing '{query}'.")

    def update_block(self, index, new_data):
        if index < 0 or index >= len(self.chain):
            print("Block not found.")
            return

        block_to_update = self.chain[index]
        print("Updating Block:")
        print(f"Index: {block_to_update.index}")
        print(f"Old Data: {block_to_update.data}")
        
        block_to_update.update_data(new_data)
        print("Block updated successfully!")

        # Recalculate the hashes of all subsequent blocks to keep chain valid
        for i in range(index + 1, len(self.chain)):
            self.chain[i].previous_hash = self.chain[i - 1].hash
            self.chain[i].hash = self.chain[i].calculate_hash()

        print("Blockchain hashes updated to maintain integrity.")

# Menu-driven interface
def main():
    my_blockchain = Blockchain()
    
    while True:
        print("\nBlockchain Menu")
        print("1. Add Block")
        print("2. Display Blockchain")
        print("3. Check Blockchain Validity")
        print("4. Search for a Block by Data")
        print("5. Update Block Data")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            data = input("Enter data for the new block: ")
            my_blockchain.add_block(data)
        elif choice == "2":
            print("\nBlockchain:")
            my_blockchain.display_chain()
        elif choice == "3":
            if my_blockchain.is_chain_valid():
                print("Blockchain is valid.")
            else:
                print("Blockchain is invalid.")
        elif choice == "4":
            query = input("Enter data to search for in the blockchain: ")
            my_blockchain.search_block(query)
        elif choice == "5":
            index = int(input("Enter the index of the block to update: "))
            new_data = input("Enter new data for the block: ")
            my_blockchain.update_block(index, new_data)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
