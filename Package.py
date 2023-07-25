class Package:
    def __init__(self, id_num, address, city, zip, deadline, weight, status, delivery_time):
        self.id_num = id_num
        self.address = address
        self.city = city
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time

    def __str__(self):
        return f"Package ID# {self.id_num} for {self.address}, {self.city}"

"""sample_package = Package(1, "13964 Flagtree Pl", "Manassas", "20112", "10:30AM", 5, "At Hub", "10AM")
print(sample_package)"""