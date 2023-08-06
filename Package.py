import CSVRead


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
        return f"Package ID# {self.id_num} for {self.address}, {self.city} due {self.deadline}"

    def update_address(self, new_addr, new_city, new_zip):
        """
        Updates address components of the package passed in.
        This is triggered if there is a change in delivery address.

        :param new_addr: package's new street address
        :param new_city: package's new city
        :param new_zip: package's new zip code
        :return:
        """
        self.address = new_addr
        self.city = new_city
        self.zipcode = new_zip

    def update_status(self, to_status, delivery_time):
        self.status = to_status
        self.delivery_time = delivery_time
        """if to_status == "En Route":
            self.status = to_status
            self.delivery_time = delivery_time
        elif to_status == "Delivered":
            self.status = to_status
            self.delivery_time = delivery_time"""

    def addr_id_lookup(self):
        return CSVRead.addr_id_lookup(self.address)