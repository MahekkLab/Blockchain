import hashlib
import json
import time

# ---------------------------
# Simple Block Structure
# ---------------------------
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


# ---------------------------
# Blockchain
# ---------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, time.time(), {"message": "Genesis Block"}, "0")
        self.chain.append(genesis)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_new_block(self, data):
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=self.last_block.hash
        )
        self.chain.append(block)
        return block


# ---------------------------
# Lost & Found System
# ---------------------------
class LostAndFoundSystem:
    def __init__(self):
        self.blockchain = Blockchain()

    def register_lost_item(self, item_id, item_name, owner_name, contact):
        data = {
            "type": "lost",
            "item_id": item_id,
            "item_name": item_name,
            "owner_name": owner_name,
            "contact": contact
        }
        return self.blockchain.add_new_block(data)

    def register_found_item(self, item_id, description, finder_name):
        data = {
            "type": "found",
            "item_id": item_id,
            "description": description,
            "finder_name": finder_name
        }
        return self.blockchain.add_new_block(data)

    def search_item(self, item_id):
        results = []
        for block in self.blockchain.chain:
            data = block.data
            if "item_id" in data and data["item_id"] == item_id:
                results.append(data)
        return results


# ---------------------------
# Menu Driven Program
# ---------------------------
system = LostAndFoundSystem()

while True:
    print("\n=== Blockchain Lost & Found System ===")
    print("1. Register Lost Item")
    print("2. Register Found Item")
    print("3. Search Item")
    print("4. View Blockchain")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        item_id = input("Item ID: ")
        item_name = input("Item Name: ")
        owner_name = input("Owner Name: ")
        contact = input("Contact: ")
        block = system.register_lost_item(item_id, item_name, owner_name, contact)
        print("Lost item added in block:", block.index)

    elif choice == "2":
        item_id = input("Item ID: ")
        desc = input("Description: ")
        finder = input("Finder Name: ")
        block = system.register_found_item(item_id, desc, finder)
        print("Found item added in block:", block.index)

    elif choice == "3":
        item_id = input("Enter Item ID to search: ")
        results = system.search_item(item_id)
        if results:
            print("Results:")
            for r in results:
                print(r)
        else:
            print("No record found for this item ID.")

    elif choice == "4":
        for block in system.blockchain.chain:
            print(vars(block))

    elif choice == "5":
        break

    else:
        print("Invalid choice!")
