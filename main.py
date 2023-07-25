import Package
import HashTable


testHash = HashTable.HashTable()
#testPackage = Package.Package(1, "195 W Oakland Ave", "Salt Lake City", 84115, "10:30 AM", 21, "At Hub", None)
#testHash.insert(testPackage.id_num, testPackage)
#print(testHash.table)
#testPackage2 = Package.Package(11, "2600 Taylorsville Blvd", "Salt Lake City", 84118, "EOD", 1, "At Hub", None)
#testHash.insert(testPackage2.id_num, testPackage2)
#print(testHash.table)

testHash.insert("Sparks", "Gunslinger")
print(testHash.table)
testHash.insert("Tetrad", "Elementalist")
print(testHash.table)
testHash.insert("Fortitude", "Warrior")
print(testHash.table)