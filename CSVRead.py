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

# Reads addresses
with open('data/addresses.csv', newline='') as addresses_csv:
    addr_reader = csv.reader(addresses_csv)
    # Each row in the CSV is the address ID number, the name of the location, and the actual address
    addr_list = [row for row in addr_reader]
# Reads in distances
with open('data/distances.csv', newline='') as distances_csv:
    dist_reader = csv.reader(distances_csv)
    # Each row in the CSV ties in with each row in the CSV.
    # Each "column" effectively makes the adjacency matrix.
    dist_list = [loc for loc in dist_reader]


def print_dist_mtx():
    for loc in dist_list:
        print(f'== {loc}')


def print_addr_list():
    for addr in addr_list:
        print(f'== {addr}')


def dist_mtx_lookup(id_a, id_b):
    """
    It will return the value found in the distance matrix.

    Should there not be a value at the coordinate specified, transposition occurs to find the value.

    Note that the ID numbering for addresses start at 0, since index counting starts at 0. It will correlate directly
    and correctly to the indices in question.
    :param id_a: first address ID (origin address ID)
    :param id_b: second address ID (destination address ID)
    :return: distance in miles as a float
    """
    if dist_list[int(id_a)][int(id_b)] == "":
        return float(dist_list[int(id_b)][int(id_a)])
    else:
        return float(dist_list[int(id_a)][int(id_b)])


def addr_id_lookup(target_addr):
    """
    Takes the street name portion of the address. Used in tandem with the distance lookup function.
    Note that the address passed in must be an address; make sure it's not a truck or package object, but
    rather, their **address attribute**.
    :param target_addr: the street name
    :return: the address ID number
    """
    for addr in addr_list:
        if addr[2] == target_addr:
            return addr[0]


def addr_name_lookup(addr_id):
    """
    A reversal of addr_id_lookup(); it will take the ID and return the appropriate address.
    :param addr_id: address ID
    :return: the street name
    """
    for addr in addr_list:
        if addr[0] == addr_id:
            return addr[2]


def print_pkg():
    """
    Prints out each line of the packages.csv file.
    :return: none
    """
    with open('data/packages.csv', newline='') as package_csv:
        pkg_reader = csv.reader(package_csv)
        for pkg in pkg_reader:
            print(f'=== {pkg}')


def add_pkgs(hash_table):
    """
    Adds all packages listed in the packages.csv file to the hash table. The ID number and weight is converted
    from a string to an integer. The rest of the fields in the CSV file are kept as a string.

    This will only run **once** throughout the program at the initial time it starts.

    - ID number is used as a key to insert into the hash table.
    - Some of the other fields build the package object to store as a value with the key it's associated with.
    :return:
    """
    with open('data/packages.csv', 'r', newline='') as package_csv:
        pkg_list = csv.reader(package_csv)  # list to for-loop through
        for row in pkg_list:  # Note that pkg is a list of values
            pkg_id = int(row[0])
            pkg_weight = int(row[6])
            gen_pkg = Package.Package(pkg_id, row[1], row[2], row[4], row[5], pkg_weight,
                                      "At or Arriving to Hub", "")
            hash_table.insert(pkg_id, gen_pkg)
