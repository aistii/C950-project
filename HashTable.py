class HashTable:
    def __init__(self, size=10, load_factor=0.8):
        self.table = [[None] for _ in range(size)]
        self.load_factor = load_factor

    @staticmethod
    def hash_func(k):
        """
        Hashes the provided key.
        :param k: key: int
        :return: hashed key
        """
        return abs(hash(k))

    def resize(self, old_table):
        """
        Creates a new hash table double the size of the old one,
        rehashes the old keys, and then inserts them into the appropriate place on the table.
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

    def insert(self, k, v):
        """
        Inserts a value into the hash table, using a key-value pair. A resize is triggered if it
        exceeds the 80% filled threshold.
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

    def search(self, k):
        """
        Searches for a package based on its key.
        :param k: key for object
        :return: the object
        """
        bucket_hash = self.hash_func(k) % len(self.table)
        bucket = self.table[bucket_hash]
        if bucket is not None:
            for kv_pair in bucket:
                if kv_pair[0] == k:
                    print(kv_pair[1])
                    return kv_pair[1]
        else:
            return None

    def update(self, k, new_properties):
        """
        This updates the package properties. ID is not mutable.
        This is a method that calls other methods to update properties.
        It does not take user input.

        **Mutable properties:**

        - Package properties, such as address components.
        - Logistics properties, such as delivery status/time, and deadline.

        :param k: key for object
        :param new_properties: new object generated from constructor passed in
        :return: none
        """
        bucket_hash = self.hash_func(k) % len(self.table)
        bucket = self.table[bucket_hash]
        if bucket is not None:
            for kv_pair in bucket:
                if kv_pair[0] == k:
                    print(f'Updating {kv_pair} value now.')

    """
    TODO: 
    - It may be better to put the setter/getter ideas into the package class
    """
    def change_addr(self, target, new_addr, new_city, new_zip):
        """
        Updates address components of an object.
        Indexes 1 through 3 (inclusive) of the package object relate to the address.

        :param target: package object to change address components
        :return: updated package object
        """
