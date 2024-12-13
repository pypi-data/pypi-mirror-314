# RecommendationLibrary

## Description
This library/package was designed to imitate the recommendation process of a friends/colleagues. It offers various features such as a storage engine, a filtering engine and a recommendation engine. All these make for a very portable recommendation library that is compatible with python and other languages since they can share data and in the long run share information.

This package/library is made up of three main drivers:

1. Storage Engine
2. Filtering Engine
3. Recommendation Engine

## Storage Engine
This part of the system deals with loading and storing information regarding the various types of features such as music, notifications, songs, artists etc.

The data that is parsed by the storage engine is supposed to be in the format below. It also has to be json data.

```json
    {
        "feature":{
            "feature_instance_id":{
                "feature-detail_1": "detail information",
                "feature-detail_2": "detail information",
                "feature-detail_3": "detail information",
            }
        }
    }
```

for example a songs feature
```json
    {
        "songs":{
            "SONG123":{
                "name": "Back Home",
                "artist": "Muhsin K",
                "number-of-views": "400000",
            }
        }
    }
```

The storage engine has the following API's

#### getSavedData()
Takes in no parameters but returns the dictionary of all saved records in the engine in the order that it had loaded all of them. 

#### viewCategoriesOfData()
Takes in no parameters but returns a list of all the features presently stored in the storage engine i.e ["songs", "movies", "notifications"]

#### returnDataInCategory(category)
Takes in a category name in form of a string. If that category doesn't exist in the engine's stored data. It returns a String "Category Doesn't Exist". Otherwise, if it exists, then it returns a list of ids of the data in that particular category

Note: The category in this case represents the same thing as the feature.

#### loadData(storagelocation)
Takes in a storagelocation in terms of a string representing a file path, whether absolute or relative. If the file exists, we proceed to check if some of the features in that file are already present in the stored data.

If they exist, the new data is simply appended to the feature already present.

If they don't exist, the new feature is added to the dictionary and the data for that feature is placed as a value for that new feature.

Note: The data being added must resemble the one illustrated below:

```json
    {
        "feature":{
            "feature_instance_id":{
                "feature-detail_1": "detail information",
                "feature-detail_2": "detail information",
                "feature-detail_3": "detail information",
            }
        }
    }
```

if the file in the path doesn't exist, an IOError is given

#### saveData(saveLocation)
This takes in the file path to save the file and writes the data present in the storage engine to the save location specified.

#### doesCategoryExist(category)
This takes in the category/feature that is to be queried and returns a boolean showing if it's present or not.

True means it exists

False means it doesn't exist

#### doesRecordExist(label)
This takes in a string of the feature_instance_id and if it is present, returns true

Otherwise it returns false.

#### getRecordWithId(id)
This takes in an id string and if there isn't an associated record/feature_instance with an id similar to the parameter, return "Record with id:{id} doesn't exist"

Otherwise it returns that record with that id

#### getRecordWithIdAndCategory(id, category)
This takes in two parameters, an ID and a category. 

First it searched if the category exists. If it doesn't exist, it returns a string with the message: "Record Doesn't Exist"

Otherwise, if the category exists but the id is not registered, then it returns a string with the message: "Record with id{id} doesn't exist"

If both exist, it returns the record with that particular ID and category in form of a dictionary object.

#### getRecordsWithIdsInCategory(ids, category)
This takes in two parameters, a list of ids and a list of categories, It then first searched for the category/feature

If that feature doesn't exist in the stored data, a string with a message "Records Don't Exist" is returned

Otherwise if the category exists, then all ids are checked for which ones exist. If an Id doesn't exist, it is appended to the list of Id's that don't exist.

If the id is present then the record that is attached to that id is placed in a list that will be returned at the end.

At the end of the execution, A tuple is returned with the list of id's that are absent as well as a list of records attached to particular ids.

The tuple's first record is that of records and then it's second record is that of absent ids.

#### getRecordsInCategory(category)
This takes in a string of the category/feature and returns a list of records in that particular feature/category

#### getAllRecords()
This takes in no parameters and returns a list of all records presently stored in the storage engine

#### getRecordsWithIdsInMultipleCategories(ids, categories)
This takes in two parameters, a list of ids and a list of categories

it returns a tuple containing records in the zero index, ids not present in the first index and categories in the second index

## Filtering Engine
This part of the system deals with filtering a set of records to only extract those that match a certain criteria. 

It is mainly used to filter data that has just come out of the storage engine before it goes into the recommendation algorithm. It mainly utilizes lists in it's everyday operation.

The filtering engine uses the following API's
#### doesLabelExist(label)
This takes in a string parameter and a list of data.

And returns True or false basing on if one of the keys in this list is the label being queried

#### getRecordsWithLabels(data, labels)
This takes in a list of data and a list of labels

And returns records in the list of data that have keys that resemble any of the labels. It returns a list

#### getRecordsWithLabel(label, data)
This takes in a list of data and a label

It returns all record in the data that have a particular label as a key

#### getLabels(data)
This takes in a list of data

This returns all unique labels present in a list of data 

#### getValuesWithSubstring(data, substring)
This takes in a list of data and a substring

This returns all values that match the substring specified. The returned values are brought back in a list

#### sortRecords(data, labeltoUse)
This takes in a list of data and sorts it in descending order in respect to the label in use

Returns a sorted list in descending order according to the values attached to the labeltoUse

Note: All lists of data as parameters should be the final level of the hierarchy for example the final level of the heirarchy below:

```json
    {
        "feature":{
            "feature_instance_id":{
                "feature-detail_1": "detail information",
                "feature-detail_2": "detail information",
                "feature-detail_3": "detail information"
            }
        }
    }
```

would be
```json
    {
        "feature-detail_1": "detail information",
        "feature-detail_2": "detail information",
        "feature-detail_3": "detail information"
    }

```

So the list would be a list of objects similar to the one above:

## Recommendation Engine
This engine is used for recommending features to users based on past user data and other criteria such as location and user history. With this engine, you can give recommendations based on user history and location in terms of x and y coordinates.

Also it requires a usermanager, filteringsystem as well as an ID to function in it's full potential. Without those, it will be difficult for it to perform it's functions.

This engine has a few api's you can use:
#### recommendationsBasedOnSimilarity(userForComparison, maximumNumberOfRecommendations)
This takes in two parameters, one optional and one compulsory: userForComparison is compulsory and maximumNumberOfRecommendations is optional.

If the user is not present in the system, the api returns "User isn't registered in the list of users. Perhaps you should recommend in terms of likes or number Of views."

The user passed in as a parameter can only have the Id set and if present in the system, the api will complete the data with the that one present in the system.

It then returns a list of recommendations based on the user given and their history. 

If the user has no history. The function will return "Try recommendations based on number of likes".

#### recommendationsBasedOnNumberOfLikes(maximum)
This takes in one optional parameter: maximum which is the maximum number of records you would like to recieve from the system.

This returns a list of recommendations based on number of likes

#### recommendationsBasedOnNumberOfViews(maximum)
This takes in one optional parameter: maximum which is the maximum number of records you would like to recieve from the system.

This returns a list of recommendations based on number of views.

Note: For number of views and Number of likes, the data stored must have a feature detail "NumberOfLikes" or "NumberOfViews"

#### recommendationBasedOnLocation(location, rangeInMeters, maximumRecommendations)
This takes in three parameters: a location, rangeInMeters(Optional) and maximumRecommendations(Optional)

If rangeInMeters is not set, we get recommendations from users in a range of 10km.

If maximumRecommendations is not set, we get a maximum of 10 recommendations.

It returns a list of recommendations based on nearby users.


#### recommendationBasedOnCategory(category, maximum)
This takes in two parameters: a category to look at and a maximum number of recommendations

If the category doesn't exist, then it returns a string with a message "Category Doesn't exist"

Otherwise it returns a list of recommendations based on number of views for that particular category

Note that recommendations come in the form of 

```python
    ["category/feature", "feature_instance_id"]
```

This is so that the user can query for the records with those particular id if need be

## Other classes that make the system work
### UserManager
This is used to manage the users in the system as well as query for specific users and histories that is paramount to the usage of recommendations based on similar histories.

The class has several API's
#### loadUsersFromFile(filelocation)
This takes in one parameter, the file location either in absolute or relative path.

It loads the user manager with the users whose data is stored in the file specified at that file location.

#### saveUsersToFile(filelocation)
This takes in one parameter, the file location to store the users data

It writes all the users and their data to the file

#### addUser(user)
This has one parameter: user. This is a user to be added in the user manager class.

#### searchForUser(id)
This takes in one parameter: id. This is the id of the user that is being searched for

if absent, a string of with the message return "User with id{id} doesn't exist"

if present, a user is returned.

#### removeUser(id)
This takes in one parameter: id. This is the id of the user to be removed.

If absent, a string with the message "User doesn't exist" is returned

If present, the removed user is returned.

#### returnUsersWithHistoryHavingRecordWithId(id)
This takes in one parameter, the id of the resource that we are looking for in one's history.

It returns users with resource with a certain id

#### returnUsersWithHistoryHavingRecordWithIdInCategory(id, category)
This takes in two parameters: id of the resource and the category to which it belongs.

It returns users that have a resource with an ID in that category.

#### getUsersWithSimilarHistories(userToCompare:User, percentage, maximum, otherUsers)
This takes in four parameters: userToCompare takes in a user, percentage similarity, maximum number of users, and other users that should be compared.

This returns a list of users that are above a certain percentage similarity.

#### getUsersInRangeOfLocation(meters, location)
This takes in two parameters: meters and location.

Returns a list of users within a certain range

#### getSortedListOfUsersBasedOnSimilarity(users, maximum)
This takes in two arguments: users that need to be sorted and a maximum number of users above the similarity threshold.

Returns a sorted list of users basing on the percentage history similarity.

#### getAllUsers()
This returns a list of all users.

#### distanceToLocationInMeters(locationOrigin,locationDestination)

This takes in two arguments: locationOrigin and locationDestination

Returns the distance in meters between the two parameters

## Location
This class handles implementation of the location based interactions.

It implements the following APIs
#### getRegion()
Returns the region presented during initialization

#### getLongitude()
Returns the longitude of the location in string form

#### getLatitude()
Returns the latitude of the location in string form

#### setLatitude(latitude)
Takes in one parameter: the latitude in string form
Sets the latitude of the location

#### setLongitude(longitude)
Takes in one parameter: the longitude in string form
Sets the longitude of the location

#### setRegion(region)
Takes in one parameter: the region in string form
Sets the region of the location

#### getLocationInFloat()
Returns a list containing the float of the latitude in zero index and the float of the longitude in the first index

#### getLocation()
Returns a tuple containing the latitude in the zero index and the longitude in the first index

### setLocation(latitude, longitude)
Takes in two parameters: latitude in string form and longitude in string form

Sets the longitude and latitude of a location

## History
This class is used to represent a history of a user

Contains records in a user's history of a feature instance that they have viewed or seen

## User
This class deals with registration of a user in the system

Contains history of a user and the user id