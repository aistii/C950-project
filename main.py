import Package
import HashTable
import CSVRead


# CSVRead.printPkg()
pkg_table = HashTable.HashTable()
CSVRead.addPkgs(pkg_table)
print(pkg_table.table)
pkg_table.search(9)



"""testHash = HashTable.HashTable()
print(testHash.table)
testPackage = Package.Package(1, "195 W Oakland Ave", "Salt Lake City", 84115, "10:30 AM", 21, "At Hub", None)
testHash.insert(testPackage.id_num, testPackage)
print(testHash.table)
testPackage2 = Package.Package(11, "2600 Taylorsville Blvd", "Salt Lake City", 84118, "EOD", 1, "At Hub", None)
testHash.insert(testPackage2.id_num, testPackage2)
print(testHash.table)
#print(testHash.search(1))
testPackage3 = Package.Package(21, "3595 Main St", "Salt Lake City", 84115, "EOD", 3, "At Hub", None)
testHash.insert(testPackage3.id_num, testPackage3)
print(testHash.table)
testHash.search(11)
#print(testHash.table)
#gunslinger = HashTable.TableItem("Sparks", "Gunslinger")
#testHash.insert("Sparks", "Gunslinger")
#(testHash.table)
gunslinger.key = "Sparks"
gunslinger.value = "Roxanne"
testHash.insert(gunslinger.key, gunslinger.value)
print(testHash.table)
testHash.insert("Tetrad", "Elementalist")
print(testHash.table)
testHash.insert("Fortitude", "Warrior")
print(testHash.table)
##testHash.search("Sparks")"""