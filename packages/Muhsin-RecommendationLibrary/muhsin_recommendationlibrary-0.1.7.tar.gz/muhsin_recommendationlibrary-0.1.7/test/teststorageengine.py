import sys

sys.path.append("/home/muhsin/Desktop/RecommendationLibrary/src")

from recommendationengine.storageengine import StorageEngine

#initialization of the Storage Engine
storageEngine = StorageEngine()

#Loading data into the storage engine
storageEngine.loadData("./test/Data/storageData.json")

# Getting all records stored in the storage engine
records = storageEngine.getAllRecords()
print(records)

#getting a record with a particular id
record = storageEngine.getRecordWithId("NOT002")
print(record)

#getting a record in a particular category with a particular id
record = storageEngine.getRecordWithIdAndCategory("NOT001", "notifications")
print(record)

#getting multiple records with multiple ids
records = storageEngine.getRecordsWithIdsInCategory(["NOT001", "NOT002", "NOT003", "NOT004"], "notifications")
print("\nRecords with ids")
print(records[0])

print("\nIDs not found")
print(records[1])

#checking if a record exists

exists = storageEngine.doesRecordExist("NOT004")
print(f"\nRecord with id NOT004 exists: {exists}")

#checking if a category exists
exists = storageEngine.doesCategoryExist("notifications")
print(f"\nCategory 'notifications' exists: {exists}")

#saving data to a file
storageEngine.saveData("./test/Data/test.json")

#getting records in a particular category
records = storageEngine.getRecordsInCategory("notifications")

print("\nRecords in category 'notifications':")
for record in records:
    print(f"\t{record}")

#getting all records
records = storageEngine.getAllRecords()

print("\nAll Records")
for record in records:
    print(f"\t{record}")

# getting records with ids in multiple categories
records = storageEngine.getRecordsWithIdsInMultipleCategories(["NOT001", "NOT002", "NOT005"], ["notifications", "beers"])

print("\nRecords Found:")

for record in records[0]:
    print(f"\t{record}")

print("\nMissing categories:")
print(f"\t{records[2]}")

print("\nMissing IDs:")
print(f"\t{records[1]}")