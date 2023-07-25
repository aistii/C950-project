class HashTable:
    def __init__(self, size=2, load_factor=0.5):
        # If exceeds 6/10 full, it will double in size down the road.
        self.table = [None] * size
        self.load_factor = load_factor

    def hash_func(self, k):
        return abs(hash(k))

    def resize(self, old_table):
        # Old table is the table to be resized
        new_size = len(old_table) * 2
        resized_table = [None] * new_size
        # Adds back in the elements, but they will be in different location
        # due to the modified modulus value
        for el in old_table:
            """
            I think the NoneType error occurred when I came across an "el" that was None.
            So there has to be a conditional check, and will only update the non null ones.
            Look at the DSA1 Zybook on hash table resizing
            """
            if el is not None:
                cur_el_hash = self.hash_func(el[0]) % len(resized_table)
                resized_table[cur_el_hash] = (el[0], el[1])
        return resized_table

    def insert(self, k, v):
        occupied_slots = sum(el is not None for el in self.table)
        current_lf = occupied_slots / len(self.table)
        if current_lf >= self.load_factor:  # trigger
            old_table = self.table
            # it first makes new table with the new values
            new_table = self.resize(old_table)
            # make new hash number with new size
            bucket_hash = self.hash_func(k) % len(new_table)
            # append to correct bucket
            new_table[bucket_hash] = (k, v)
            # make this new table this instance's default table
            self.table = new_table
        else:
            bucket_hash = self.hash_func(k) % len(self.table)
            self.table[bucket_hash] = (k, v)

    def search(self, k):
        bucket_hash = self.hash_func(k) % len(self.table)
        bucket = self.table[bucket_hash]
        if bucket is not None:
            return bucket[1]
        else:
            return None
