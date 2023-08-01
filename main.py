# Leanna Garner === Student ID 010636491 === C950 Project
import datetime
import Package
import HashTable
import CSVRead
import Truck
import sys

"""
=== INITIALIZATION ===
This portion creates a hash table, adds packages to it,
and then creates truck objects so that the package IDs can be stored in them.

$$$ I could've simply passed in a list for the trucks' package lists, but
I thought that loading each package itself would be better. It updates the
package status too, because it's using the hash table's search function which
does return the package object itself, so it takes care of two things at once.
"""

pkg_table = HashTable.HashTable()
CSVRead.add_pkgs(pkg_table)
truck_1 = Truck.Truck(1, datetime.timedelta(hours=8, minutes=0, seconds=0))  # Leaves at 8AM
truck_2 = Truck.Truck(2, datetime.timedelta(hours=9, minutes=5, seconds=0))  # Leaves at 9:05AM
truck_3 = Truck.Truck(3, None)  # Will leave when one of the other trucks comes back
pkg_set_1 = [39, 13, 8, 30, 37, 1, 4, 40, 21, 20, 31, 19, 14, 16, 34, 15]
pkg_set_2 = [3, 5, 38, 36, 17, 6, 28, 2, 33, 12, 32, 25, 18, 11, 25, 26]
pkg_set_3 = [7, 29, 10, 27, 33, 24, 22, 9]
for pkg in pkg_set_1:
    truck_1.load_pkg(pkg_table.search(pkg))
for pkg in pkg_set_2:
    truck_2.load_pkg(pkg_table.search(pkg))
for pkg in pkg_set_3:
    truck_3.load_pkg(pkg_table.search(pkg))



"""
=== ALGORITHM ===
Since package loading was handled manually, the algorithm below is to find
the most appropriate route to deliver the packages, using the nearest-neighbor algorithm.

$$$ I think I could've created an algorithm to load, since I loaded them 
according to their constraints primarily (those with a deadline should have 
higher priority for delivery) and what packages could be delivered that were nearby 
or at the same address as those packages.
"""