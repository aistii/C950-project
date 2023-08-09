"""
Class file for hash table.
"""

import Package


class HashTable:
    """
    The hash table holds package information inserted in. Chaining is enabled and will resize if the load factor
    exceeds 80% full.

    A hash table instance has a space complexity of O(N) - linear.
    """
    def __init__(self, size=10, load_factor=0.8):
        self.table = [[None] for _ in range(size)]
        self.load_factor = load_factor

    @staticmethod
    def hash_func(k):
        """
        Hashes the provided key.

        **Time Complexity:** O(1) - constant
        :param k: key
        :return: hashed key
        """
        return abs(hash(k))

    def resize(self, old_table):
        """
        Creates a new hash table double the size of the old one,
        rehashes the old keys, and then inserts them into the appropriate place on the table.

        **Time Complexity:** O(N) - linear
        :param old_table: old hash table with values
        :return: blank resized table
        """
        new_size = len(old_table) * 2
        resized_table = [[None] for _ in range(new_size)]
        for old_bucket in old_table:
            if old_bucket != [None]:
                for kv_pair in old_bucket:
                    cur_bucket_hash = self.hash_func(kv_pair[0]) % len(resized_table)
                    resized_table[cur_bucket_hash] = [[kv_pair[0], kv_pair[1]]]
        return resized_table

    def insert(self, k: int, v: Package.Package):
        """
        Inserts a value into the hash table, using a key-value pair. A resize is triggered if it
        exceeds the 80% filled threshold.

        **Time Complexity:** O(N) - linear (worst case due to potentially resizing)
        :param k: package id
        :param v: package object
        :return: nothing
        """
        occupied_slots = 0
        for bucket in range(0, len(self.table)):
            is_occupied = (self.table[bucket] != [None])
            if is_occupied:
                occupied_slots += 1
        current_lf = occupied_slots / len(self.table)
        if current_lf >= self.load_factor:
            old_table = self.table
            new_table = self.resize(old_table)
            bucket_hash = self.hash_func(k) % len(new_table)
            self.table = new_table
            if self.table[bucket_hash] == [None]:
                self.table[bucket_hash] = [[k, v]]
        else:
            bucket_hash = self.hash_func(k) % len(self.table)
            self.table[bucket_hash] = [[k, v]]

    def search(self, k: int):
        """
        Searches for a package based on its key.

        **Time Complexity:** O(N) - linear
        :param k: key for object
        :return: the object
        """
        bucket_hash = self.hash_func(k) % len(self.table)
        bucket = self.table[bucket_hash]
        if bucket is not None:
            for kv_pair in bucket:
                if kv_pair[0] == k:
                    return kv_pair[1]
        else:
            return None
