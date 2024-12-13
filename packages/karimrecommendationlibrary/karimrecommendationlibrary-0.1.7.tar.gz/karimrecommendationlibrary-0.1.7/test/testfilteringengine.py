import sys

sys.path.append("/home/muhsin/Desktop/RecommendationLibrary/src")

from recommendationengine.filteringengine import FilteringEngine
from recommendationengine.storageengine import StorageEngine
#initializing a storage engine to provide us with data to manipulate
storage = StorageEngine("./test/Data/storageData.json")

#getting all data in storage
StorageRecords = storage.getAllRecords()

#initializing a filtering engine
filter = FilteringEngine()

##Finding out whether a label exists
labelexists = filter.doesLabelExist("Message", StorageRecords)

if labelexists == True:
    print("Label Exists")

else:
    print("Label Not Present")

#getting records with a particular label
records = filter.getRecordsWithLabels(["Message", "NumberOfLikes"], StorageRecords)

print("\nRecords with labels: 'Message' or 'NumberOfLikes'")

for record in records:
    print(f"\n{record}")

#getting records that have a particular label
records = filter.getRecordsWithLabel("Message", StorageRecords)

print("\nRecords with label: 'Message'")

for record in records:
    print(f"\n{record}")

#getting all labels in data provided
labels = filter.getLabels(StorageRecords)

print("\nAll labels")

for label in labels:
    print(f"\t{label}")

#getting records that have a particular value
values = filter.getValuesWithSubstring(StorageRecords, "Karim")

print("\nAll values")

for value in values:
    print(f"\t{value}")

#sorted records based on a feature description

values = filter.sortRecords(StorageRecords, "NumberOfLikes")

print("\nSorted Records")

for value in values:
    print(f"\t{value}")