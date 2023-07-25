# The Hash Table Item will take in the key and the value.
# Maybe the key will be borrowed from the value (the package object)?
class HashTableItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    """def __repr__(self):
        return f"({self.key}, {self.value})"""


class HashTable:
    def __init__(self, initial_capacity=10):
        self.table = [None] * initial_capacity

    def hash_key(self, key):
        return abs(hash(key)) % len(self.table)

    def insert(self, key, value):
        bucket_index = self.hash_key(key)
        item = self.table[bucket_index]
        previous = None
        while item != None:
            if key == item.key:
                item.value = value
                return True
            previous = item
            item = item.next
        if self.table[bucket_index] == None:
            self.table[bucket_index] = HashTableItem(key, value)
        else:
            previous.next = HashTableItem(key, value)
        return True

    def remove(self, key):
        bucket_index = self.hash_key(key)
        item = self.table[bucket_index]
        previous = None
        while item != None:
            if key == item.key:
                if previous == None:
                    self.table[bucket_index] = item.next
                else:
                    previous.next = item.next
                return True
            previous = item
            item = item.next
        return False

    def search(self, key):
        bucket_index = self.hash_key(key)
        item = self.table[bucket_index]
        while item != None:
            if key == item.key:
                return item.value
            item = item.next
        return None

    def __str__(self):
        result = ""
        for i in range(len(self.table)):
            result += "%d: " % i
            if self.table[i] == None:
                result += "(empty)\n"
            else:
                item = self.table[i]
                while item != None:
                    result += "%s, %s --> " % (str(item.key), str(item.value))
                    item = item.next
                result += "\n"
        return result

"""keyw = "123"
print(f"test hash key random: {abs(hash(keyw))}")
testHash = HashTable()
testHash.insert(1, "potato")
print(testHash.table)
testHash.insert(1, "strawberry")
print(testHash.table)
testHash.insert("food", "ramen")
print(testHash.table)
print(testHash.search("food"))
testHash.remove(1)
print(testHash.table)"""