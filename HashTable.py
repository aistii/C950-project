class HashTable:
    def __init__(self, size=1, load_factor=0.5):
        # If exceeds 6/10 full, it will double in size down the road.
        self.table = [[None] for _ in range(size)]
        self.load_factor = load_factor

    def hash_func(self, k):
        return abs(hash(k))

    def resize(self, old_table):
        # Old table is the table to be resized
        print(f"(resize) old table length: {len(old_table)}")
        new_size = len(old_table) * 2
        resized_table = [[None] for _ in range(new_size)]
        print(f"(resize) resized table: {resized_table}")
        # Adds back in the elements, but they will be in different location
        # due to the modified modulus value
        for old_bucket in old_table:
            """
            I think the NoneType error occurred when I came across an "el" that was None.
            So there has to be a conditional check, and will only update the non null ones.
            Look at the DSA1 Zybook on hash table resizing
            """
            print(f"(resize) !current old bucket contents (KV pairs list): {old_bucket}")
            if old_bucket != [None]: # If the bucket is occupied by at least one KV pair
                for kv_pair in old_bucket:
                    print(f"(resize) bucket key: {kv_pair[0]}")
                    print(f"(resize) bucket value: {kv_pair[1]}")
                    cur_bucket_hash = self.hash_func(kv_pair[0]) % len(resized_table)
                    print(f"(resize) current bucket hash: {cur_bucket_hash}")
                    resized_table[cur_bucket_hash] = [[kv_pair[0], kv_pair[1]]]
                    print(f"(resize) resized: {resized_table}")

        return resized_table

    def insert(self, k, v):
        print(f"(insert) Table is this buckets big: {len(self.table)}")
        """occupied_slots = sum(el is not [None] for el in self.table)"""
        occupied_slots = 0
        for bucket in range(0, len(self.table)):
            print(f"(insert) Iter #{bucket} has '{self.table[bucket]}' inside pre-insert.")
            print(f"(insert) Is bucket occupied with something other than [None]?\n"
                  f"=== {self.table[bucket] != [None]}")
            is_occupied = (self.table[bucket] != [None])
            if is_occupied:
                occupied_slots += 1
        print(f"(insert) Number of occupied slots: {occupied_slots}")
        current_lf = occupied_slots / len(self.table)
        if current_lf >= self.load_factor:  # trigger
            old_table = self.table
            # it first makes new table with the new values
            new_table = self.resize(old_table)
            print(f"(insert) new table: {new_table}")
            # make new hash number with new size
            bucket_hash = self.hash_func(k) % len(new_table)
            print(f"(insert) bucket hash: {bucket_hash}")
            # make this new table this instance's default table
            self.table = new_table
            print(f"(insert) updated table: {self.table}")
            # append to correct bucket, move to different one if it's not empty
            if self.table[bucket_hash] is None:
                print("(insert) First entry in bucket doing")
                self.table[bucket_hash] = [k, v]
            else:
                print(f"(insert) Appending to bucket: {self.table[bucket_hash]}")
                self.table[bucket_hash].append([k, v])

        else:
            print(f"(insert) length of table: {len(self.table)}")
            bucket_hash = self.hash_func(k) % len(self.table)
            print(f"(insert) insert else's branch hash: {bucket_hash}")

            self.table[bucket_hash] = [[k, v]]

    def search(self, k):
        bucket_hash = self.hash_func(k) % len(self.table)
        print(f"(search) bucket hash is {bucket_hash}")
        bucket = self.table[bucket_hash]
        print(f"(search) looking in this bucket: {bucket}")
        if bucket is not None:
            print(f"(search) * Bucket: {bucket}")
            for item in bucket:
                print(f"(search) == Current Item: {item}")
                if item[0] == k:
                    return item[1]

        else:
            return None
