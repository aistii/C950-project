import HashTable
import Package
import CSVRead
import datetime


class Truck:
    speed: int = 18
    max_pkg: int = 16

    def __init__(self, truck_number: int, departure_time):
        self.truck_num: int = truck_number
        self.pkg_list = []
        self.odo: int = 0  # Miles traveled so far
        self.current_addr = "4001 South 700 East"
        self.departure_time = departure_time  # When the truck actually leaves the hub.
        self.current_time = None

    def load_pkg(self, package: Package.Package):
        """
        Loads the package onto the truck. It will mark the package as "En Route".
        It is triggered when program initially loads packages onto the truck.

        This list only stores package IDs, not the package objects themselves.

        :param package: package to load onto the truck
        :return:
        """
        pkg_id = package.id_num
        self.pkg_list.append(pkg_id)
        package.update_status("En Route", "")

    def denote_delivered(self, pkg_id: int, hash_table: HashTable.HashTable):
        """
        Marks the package as delivered and removes package from the truck's to-deliver list.

        This looks up the ID first to update it.

        It requires a time of delivery, but I don't know how I'm implementing it yet, so I'm just writing
        it as an empty string for now.

        :param pkg_id: id of package to update
        :param hash_table: table to look up the object
        :return:
        """
        delivered_package: Package.Package = hash_table.search(pkg_id)
        delivered_package.update_status("Delivered", "")
        self.pkg_list.remove(pkg_id)

    def fetch_curr_addr_id(self):
        print(self.current_addr)
        return CSVRead.addr_id_lookup(self.current_addr)
