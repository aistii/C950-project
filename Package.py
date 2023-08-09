"""
A class file that holds information about packages, including address information, physical properties,
and status. It includes several methods to update or lookup certain package information.
"""

import CSVRead


class Package:
    """
    Holds information about packages, including address information, physical properties,
    and status. It includes several methods to update or lookup certain package information.

    An instance of a package has a space complexity of O(1) - constant.
    """
    def __init__(self, id_num, address, city, zipcode, deadline, weight, status):
        self.id_num = id_num
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.delivery_time = None
        self.departure_time = None

    def __str__(self):
        return f"Package ID# {self.id_num} for {self.address}, {self.city} due {self.deadline}"

    def update_address(self, new_addr, new_city, new_zip):
        """
        Updates address components of the package passed in.
        This is triggered if there is a change in delivery address.

        **Time Complexity:** O(1) - constant
        :param new_addr: package's new street address
        :param new_city: package's new city
        :param new_zip: package's new zip code
        :return:
        """
        self.address = new_addr
        self.city = new_city
        self.zipcode = new_zip

    def update_status(self, to_status, delivery_time):
        """
        Updates the package's status.

        **Time Complexity:** O(1) - constant
        :param to_status: new status
        :param delivery_time: the time of delivery (None if not yet delivered)
        :return:
        """
        self.status = to_status
        self.delivery_time = delivery_time

    def addr_id_lookup(self):
        """
        Returns the package's address ID.

        **Time Complexity:** O(N) - linear
        :return: package's address ID
        :rtype: int
        """
        return CSVRead.addr_id_lookup(self.address)