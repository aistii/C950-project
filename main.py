# Leanna Garner === Student ID 010636491 === C950 Project
import datetime
import Package
import HashTable
import CSVRead
import Truck

pkg_table = HashTable.HashTable()
CSVRead.add_pkgs(pkg_table)
truck_1 = Truck.Truck(1, datetime.timedelta(hours=8, minutes=0, seconds=0))  # Leaves at 8AM
truck_2 = Truck.Truck(2, datetime.timedelta(hours=9, minutes=5, seconds=0))  # Leaves at 9:05AM
truck_3 = Truck.Truck(3, None)  # Will leave when one of the other trucks comes back
pkg_set_1 = [39, 13, 8, 30, 37, 1, 4, 40, 21, 20, 31, 19, 14, 16, 34, 15]
pkg_set_2 = [3, 5, 38, 36, 17, 6, 28, 2, 33, 12, 29, 25, 18, 11, 26, 23]
pkg_set_3 = [7, 32, 10, 27, 35, 24, 22, 9]
for pkg in pkg_set_1:
    truck_1.load_pkg(pkg_table.search(pkg))
for pkg in pkg_set_2:
    truck_2.load_pkg(pkg_table.search(pkg))
for pkg in pkg_set_3:
    truck_3.load_pkg(pkg_table.search(pkg))


def sorted_by_time(pkg_list: list):
    """
    Sorts a truck's list by the time. It will move all EOD deadline packages to the end of the list.
    :param pkg_list: list to sort
    :return: sorted list of packages
    :rtype: list[Package.Package]
    """
    new_list: list[Package.Package] = []
    for pkg in pkg_list:
        pkg_obj = pkg_table.search(pkg)
        new_list.append(pkg_obj)

    def time_sort(pkg: Package.Package):
        """
        A function to act as a key by sorting by time.

        **Time Complexity:** O(1)

        :param pkg: package
        :return: package's deadline
        """
        return pkg.deadline

    def eod_pick(pkg: Package.Package):
        """
        A function to act as a filter to find which are marked as "EOD".

        **Time Complexity:**

        :param pkg: package
        :return: boolean if package has EOD deadline
        """
        return pkg.deadline == "EOD"

    eod_list = list(filter(eod_pick, new_list))
    for pkg in eod_list:
        new_list.remove(pkg)
    new_list = list(sorted(new_list, key=time_sort, reverse=True) + eod_list)
    return new_list


def combined_odo():
    """
    Totals all three trucks' mileage for this program.

    **Time Complexity:**
    :return: sum of all three trucks' mileage
    :rtype: float
    """
    return truck_1.odo + truck_2.odo + truck_3.odo


def find_nearest_neighbor(current_addr: int, remaining_list: list[Package.Package], truck: Truck.Truck):
    """
    Finds the closest node to the current address.

    Uses the distance matrix to find the closest address.

    It does not account for the possibility that the closest package is at the same node,
    that will be taken cared of in create_route(). It doesn't look at the time constraints, either.

    **Time Complexity:**
    :param current_addr: current address' ID number
    :param remaining_list: list of packages left (package objects)
    :param truck: truck object detail to change current address + count mileage
    :return: package that is closest and miles
    :rtype: Package.Package
    """
    closest_node: Package.Package = None
    closest_address_id: int = None  # Holds ID of the current closest address
    closest_address_distance: float = None  # Holds the actual shortest distance from current node
    for pkg in remaining_list:
        destination_addr_id = pkg.addr_id_lookup()
        spec_addr_distance = CSVRead.dist_mtx_lookup(current_addr, destination_addr_id)
        if closest_address_id is None:
            # If the variable is None, initialize it to the first package it comes across.
            closest_address_id = destination_addr_id
            closest_node = pkg
            closest_address_distance = spec_addr_distance
        elif spec_addr_distance < closest_address_distance:
            # If the current iteration has closer address, replace the past ID with this one
            closest_address_id = destination_addr_id
            closest_node = pkg
            closest_address_distance = spec_addr_distance
    add_to_odo(closest_address_distance, truck)
    time_taken = truck.calc_time_taken(closest_address_distance)
    arrival_time = truck.update_cur_time(time_taken)
    truck.denote_delivered(closest_node.id_num, pkg_table, arrival_time)
    return closest_node


def find_same_addr(pkg_list: list[int], addr):
    """
    Creates a list of packages that have the same address.

    **Time Complexity:**
    :param pkg_list: list of package IDs
    :param addr: address to search for
    :return: list of packages with the same IDs
    :rtype: list[Package.Package]
    """
    same_addr_list = []
    for pkg in pkg_list:
        package: Package.Package = pkg_table.search(pkg)
        this_pkg_addr = package.address
        if this_pkg_addr == addr:
            same_addr_list.append(package)
    return same_addr_list


def create_route(pkg_list: list[int], truck: Truck.Truck):
    """
    Creates the route given the list of packages and the truck.

    **Time Complexity:**
    :param pkg_list: The original loading list for the truck that contains only IDs
    :param truck: The truck being used
    :return: a list of pkg id to visit in that order
    :rtype: list[int]
    """
    output_route = []
    truck_pkg_obj_list = [pkg_table.search(package) for package in pkg_list]
    dummy_list = pkg_list.copy()  # To not mutate original list
    current_addr = truck.fetch_curr_addr_id()  # Initially the WGU hub, uses the ID number
    while len(dummy_list) > 0:
        temp_list = []  # stores all id num to insert into the list
        chosen_package = find_nearest_neighbor(current_addr, truck_pkg_obj_list, truck)  # Has its delivery time
        temp_list.append(chosen_package.id_num)  # appending the nearest package first
        dummy_list.remove(chosen_package.id_num)
        truck_pkg_obj_list.remove(chosen_package)
        same_addr_pkg_list = find_same_addr(dummy_list, chosen_package.address)
        for pkg in same_addr_pkg_list:
            truck.denote_delivered(pkg.id_num, pkg_table, chosen_package.delivery_time)
            temp_list.append(pkg.id_num)  # appending same addresses afterwards
            dummy_list.remove(pkg.id_num)
            truck_pkg_obj_list.remove(pkg)
        current_addr = CSVRead.addr_id_lookup(chosen_package.address)  # reassign
        truck.current_addr = CSVRead.addr_name_lookup(current_addr)
        for pkg_id in temp_list:
            output_route.append(pkg_id)
    return output_route


def add_to_odo(mileage: float, truck: Truck.Truck):
    """
    Adds to the truck's odometer to increase miles traveled.

    **Time Complexity:**
    :param mileage: miles traveled
    :param truck: truck that traveled
    :return: None
    """
    truck.odo += mileage


def return_truck(truck_a: Truck.Truck, truck_b: Truck.Truck):
    """
    Determines which truck to send back to the hub based on distance.

    **Time Complexity:**
    :param truck_a: truck A
    :param truck_b: truck B
    :return: chosen truck to send back to hub
    :rtype: Truck.Truck
    """
    truck_a_distance_from_hub = CSVRead.dist_mtx_lookup(0, CSVRead.addr_id_lookup(truck_a.current_addr))
    truck_b_distance_from_hub = CSVRead.dist_mtx_lookup(0, CSVRead.addr_id_lookup(truck_b.current_addr))

    if truck_a_distance_from_hub <= truck_b_distance_from_hub:
        truck_a.current_addr = CSVRead.addr_name_lookup(0)  # Make the truck "travel" back
        add_to_odo(truck_a_distance_from_hub, truck_a)  # Add the mileage to odometer for travel
        new_time = truck_a.calc_time_taken(truck_a_distance_from_hub)
        truck_a.update_cur_time(new_time)
        returning_truck = truck_a
    else:
        truck_b.current_addr = CSVRead.addr_name_lookup(0)  # Make the truck "travel" back
        add_to_odo(truck_b_distance_from_hub, truck_b)  # Add the mileage to odometer for travel
        new_time = truck_b.calc_time_taken(truck_b_distance_from_hub)
        truck_b.update_cur_time(new_time)
        returning_truck = truck_b
    return returning_truck


def menu_control(choice):
    """
    Handles the user's input for which action the program should perform.
    :param choice: the user's input
    :return: boolean if there was an error with reading the input
    :rtype: bool
    """
    def time_check(user_input):
        try:
            (h, m, s) = user_input.split(":")
            converted_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            return True
        except ValueError:
            return False

    def id_check(user_input):
        try:
            id_num = int(user_input)
            return True
        except ValueError:
            return False

    if choice == "1":  # Search with a PKG id and provide time
        pkg_id = input("Enter a valid ID number (1-40): ")
        while not id_check(pkg_id) or int(pkg_id) not in range(1, 41):
            print("🚫\tPlease enter an integer between 1 and 40.")
            pkg_id = input("Enter a valid ID number (1-40): ")
        pkg_id = int(pkg_id)
        chosen_package: Package.Package = pkg_table.search(pkg_id)
        time_of_pkg = input("Enter a time with the HH:MM:SS format, using 24-hour time: ")
        while not time_check(time_of_pkg):
            print("🚫\tPlease enter valid, correctly formatted time.")
            time_of_pkg = input("Enter a time with the HH:MM:SS format, using 24-hour time: ")
        (h, m, s) = time_of_pkg.split(":")
        converted_user_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        if converted_user_time < chosen_package.departure_time:
            d_str = f"is at or arriving to hub."
        elif chosen_package.departure_time < converted_user_time < chosen_package.delivery_time:
            d_str = f"is in transit."
        else:
            d_str = f"was delivered at {chosen_package.delivery_time}"
        print(f'{"=" * 80}\n'
              f'📦\t Package {chosen_package.id_num} Details @ {converted_user_time}:\n'
              f'\t - Address: {chosen_package.address}, {chosen_package.city}, {chosen_package.zipcode}\n'
              f'\t - Weight: {chosen_package.weight}kg\n'
              f'\t - Delivery Deadline: {chosen_package.deadline}\n'
              f'\t - Status: Package {d_str}.\n'
              f'{"=" * 80}')
        user_selection()

    if choice == "2":  # Search for all at a specific time
        time_of_pkg = input("Enter a time with the HH:MM:SS format, using 24-hour time: ")
        while not time_check(time_of_pkg):
            print("🚫\tPlease enter valid, correctly formatted time.")
            time_of_pkg = input("Enter a time with the HH:MM:SS format, using 24-hour time: ")
        (h, m, s) = time_of_pkg.split(":")
        converted_user_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        for pkg_id in range(1, 41):
            cur_pkg = pkg_table.search(pkg_id)
            if (converted_user_time < cur_pkg.departure_time) or (cur_pkg.departure_time is None):
                d_str = f"is at or arriving to hub."
            elif cur_pkg.departure_time < converted_user_time < cur_pkg.delivery_time:
                d_str = f"is in transit."
            else:
                d_str = f"was delivered at {cur_pkg.delivery_time}."
            print(f'{"=" * 80}\n'
                  f'📦\t Package {cur_pkg.id_num} Details @ {converted_user_time}:\n'
                  f'\t - Address: {cur_pkg.address}, {cur_pkg.city}, {cur_pkg.zipcode}\n'
                  f'\t - Weight: {cur_pkg.weight}kg\n'
                  f'\t - Delivery Deadline: {cur_pkg.deadline}\n'
                  f'\t - Status: Package {d_str}\n'
                  f'{"=" * 80}')
        user_selection()

    if choice == "3":  # Print everything
        for pkg_id in range(1, 41):
            cur_pkg = pkg_table.search(pkg_id)
            d_str = f"was delivered at {cur_pkg.delivery_time}."
            print(f'{"=" * 80}\n'
                  f'📦\t Package {cur_pkg.id_num} Details @ EOD:\n'
                  f'\t - Address: {cur_pkg.address}, {cur_pkg.city}, {cur_pkg.zipcode}\n'
                  f'\t - Weight: {cur_pkg.weight}kg\n'
                  f'\t - Delivery Deadline: {cur_pkg.deadline}\n'
                  f'\t - Status: Package {d_str}\n'
                  f'{"=" * 80}')
        print(f'Total Mileage: {combined_odo()}')
        user_selection()

    if choice == "Qq":  # Quit Program
        print("Goodbye!")
        exit()
    return True


def user_selection():
    """
    Handles the portion of the CLI to display program options
    and will prompt the user again if the input was not valid.
    :return: nothing
    """
    print("\nSelect from 1, 2, or 3 to view data, or select 'Q' to quit.\n"
          "[1] Single package details at a certain time\n"
          "[2] All package details at a certain time\n"
          "[3] All package details + total mileage at the end of day\n"
          "[Q] Quit the program")
    user_choice = input("Choose 1, 2, 3, or Q: ")
    while user_choice not in "123Qq":
        print("🚫\tPlease choose a valid option.")
        user_choice = input("\tChoose 1, 2, 3, or Q: ")
    menu_control(user_choice)


truck_1_route = create_route(pkg_set_1, truck_1)
truck_2_route = create_route(pkg_set_2, truck_2)
truck_returning = return_truck(truck_1, truck_2)
truck_3.departure_time = datetime.timedelta(hours=10, minutes=20, seconds=0)
truck_3.current_time = truck_3.departure_time
for pkg in truck_3.pkg_list:
    pkg_obj = pkg_table.search(pkg)
    pkg_obj.departure_time = truck_3.departure_time
package_9: Package.Package = pkg_table.search(9)
package_9.update_address("410 S State St", "Salt Lake City", "84111")
truck_3_route = create_route(pkg_set_3, truck_3)


print("================================="
      "\n🚛 Welcome to WGUPS Delivery 🚛"
      "\n=================================")
user_selection()
