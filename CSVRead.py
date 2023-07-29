"""
CSVRead does these things:

1) Utilizing the Package module and HashTable module, it will make
   insert packages read in from the data/packages.csv file to the hash table,
   using the package's ID number for the key and the generated package object
   as the key's value.
2) Associate the values from both data/distances.csv and addresses.csv in the order that they
   appear (since the distances to each location are effectively on the same line as the origin address
   they talk about in the addresses.csv file).
   - This is represented as a 2-dimensional matrix:
        - distance_matrix[x][y], where:
            - "x" represents the line in addresses.csv of the origin address
            - "y" represents the line in addresses.csv of the destination address
   - If the value in "distances.csv" does not contain a value, since only the bottom portion
     of the original matrix in the .xlsx file was filled in:
        - given distance_matrix[x][y], where "y" is empty, null, or none:
            - determine the value if the matrix was transposed, which is:
                - distance_matrix[y][x], assuming "y" and "x" are the same pair of addresses
                  prior to transposition.
"""
import csv
import Package
import HashTable


def printPkg():
    """
    Prints out each line of the packages.csv file.
    :return: none
    """
    print(f"\n (CSVRead/printPkg()) || Printing list of packages:\n")
    with open('data/packages.csv', newline='') as package_csv:
        pkg_reader = csv.reader(package_csv)
        for pkg in pkg_reader:
            print(f'=== {pkg}')

def addPkgs(hash_table):
    """
    Adds all packages listed in the packages.csv file to the hash table. The ID number and weight is converted
    from a string to an integer. The rest of the fields in the CSV file are kept as a string.

    This will only run **once** throughout the program at the initial time it starts.

    - ID number is used as a key to insert into the hash table.
    - Some of the other fields build the package object to store as a value with the key it's associated with.
    :return:
    """
    print(f"\n (CSVRead/addPkgs()) || Adding packages from file.\n")
    with open('data/packages.csv', 'r', newline='') as package_csv:
        pkg_list = csv.reader(package_csv) # list to for-loop through
        for row in pkg_list: # Note that pkg is a list of values
            pkg_id = int(row[0])
            pkg_weight = int(row[6])
            # Package defaults to "At or Arriving to Hub" and has no delivery time yet.
            # Status and delivery time are variable throughout algorithm implementation.
            # Address may change if there is incorrect address.
            gen_pkg = Package.Package(pkg_id, row[1], row[2], row[4], row[5], pkg_weight,
                                      "At or Arriving to Hub", "")
            hash_table.insert(pkg_id, gen_pkg)