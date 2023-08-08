import HashTable
import Package
import CSVRead
import datetime


class Truck:
    speed: int = 18  # Miles per hour

    def __init__(self, truck_number: int, departure_time: datetime.timedelta):
        self.truck_num: int = truck_number
        self.pkg_list = []
        self.odo: int = 0  # Miles traveled so far
        self.current_addr = "4001 South 700 East"  # Trucks will start at the WGU hub
        self.departure_time: datetime.timedelta = departure_time  # When the truck actually leaves the hub.
        self.current_time: datetime.timedelta = departure_time  # Current "time" of the truck

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
        package.update_status("En Route", None)
        package.departure_time = self.departure_time

    def denote_delivered(self, pkg_id: int, hash_table: HashTable.HashTable, delivery_time: datetime.timedelta):
        """
        Marks the package as delivered.

        This looks up the ID first to update it.

        :param pkg_id: id of package to update
        :param hash_table: table to look up the object
        :param delivery_time: time of delivery
        :return:
        """
        delivered_package: Package.Package = hash_table.search(pkg_id)
        delivered_package.update_status("Delivered", delivery_time)
        self.pkg_list.remove(pkg_id)

    def fetch_curr_addr_id(self):
        """
        Provides the address ID of the truck's location.
        :return: address ID number
        """
        return CSVRead.addr_id_lookup(self.current_addr)

    def calc_time_taken(self, miles: float):
        """
        Calculates how long it will take the package to arrive to destination.
        :param miles: miles traveled
        :return: current time
        """
        dec_time_taken = miles / self.speed  # Decimal time in hours
        hrs = int(dec_time_taken)
        mins = (dec_time_taken * 60) % 60
        secs = (dec_time_taken * 3600) % 60
        return datetime.timedelta(hours=hrs, minutes=mins, seconds=secs)

    def update_cur_time(self, time: datetime.timedelta):
        """
        Updates the current time of the truck.
        :param time: time taken
        :return: new current time
        """
        self.current_time += time
        return self.current_time
