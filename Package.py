class Package:
    def __init__(self, id_num, address, city, zipcode, deadline, weight, status, delivery_time):
        self.id_num = id_num
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.delivery_time = delivery_time

    def __str__(self):
        return f"Package ID# {self.id_num} for {self.address}, {self.city}"