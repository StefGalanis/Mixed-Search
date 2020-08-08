#Stefanos Galanis 2032
import sys
import time
import numpy as np

def kwSearchRaw(keywords,restaurants):

    restaurantsList = []

    for line in restaurants:

        lineValues = line.split('\t')
        tags = lineValues[2]

        tagsLength = len(tags)
        tags = tags[6:tagsLength-1].split(',')

        matchedKeywords = 0
        for keyword in keywords:
            if keyword in tags:
                matchedKeywords += 1

        if len(keywords) == matchedKeywords:
            restaurantsList.append(line)

    if len(restaurantsList) > 0:
        return restaurantsList
    else:
        return restaurantsList


def spaSearchGrid(queryRange,lengthX,lengthY,minX,minY):

    fragSizeX = lengthX/50
    fragSizeY = lengthY/50

    lowerBoundX = queryRange[0] - minX
    upperBoundX = queryRange[1] - minX
    lowerBoundY = queryRange[2] - minY
    upperBoundY = queryRange[3] - minY

    upperBoundX = int(upperBoundX/fragSizeX)
    lowerBoundX = int(lowerBoundX/fragSizeX)

    if upperBoundX == 50:
        upperBoundX -= 1
    if lowerBoundX == 50:
        lowerBoundX -= 1
    if upperBoundY == 50:
        upperBoundY -= 1
    if lowerBoundY == 50:
        lowerBoundY -= 1

    upperBoundY = int(upperBoundY/fragSizeY)
    lowerBoundY = int(lowerBoundY/fragSizeY)

    restaurantsToRetrieve = []

    for i in range(lowerBoundX,upperBoundX+1):
        for j in range(lowerBoundY,upperBoundY+1):
            if grid[i][j] != None:
                restaurants = grid[i][j]
                for restaurantID in restaurants:
                    restaurantsToRetrieve.append(int(restaurantID))

    restaurantsInGrid = []
    for restaurantID in restaurantsToRetrieve:
        restaurantsInGrid.append(restaurantsList[int(restaurantID)].replace('\n',''))

    
    restaurantsToReturn = []
    for restaurant in restaurantsInGrid:
        values = restaurant.split('\t')
        coordinates = values[1]
        coordinates = coordinates[9:len(coordinates)]
        coordinates = coordinates.strip().split(',')
        
        xCoordinate = float(coordinates[0])
        yCoordinate = float(coordinates[1])
        
        if xCoordinate >= queryRange[0] and xCoordinate <= queryRange[1] and yCoordinate >= queryRange[2] and yCoordinate <= queryRange[3]:
            restaurantsToReturn.append(restaurant)


    return restaurantsToReturn


def spaSearchRaw(queryRange,restaurants):

    lowerX = queryRange[0]
    upperX = queryRange[1]
    lowerY = queryRange[2]
    upperY = queryRange[3]

    resultList = []

    for line in restaurants:
        lineValues = line.split('\t')
        coordinates = lineValues[1]
        coordinates = coordinates[9:len(coordinates)]
        coordinates = coordinates.strip().split(',')


        xCoordinate = float(coordinates[0])
        yCoordinate = float(coordinates[1])
        
        if xCoordinate >= lowerX and xCoordinate <= upperX and yCoordinate >= lowerY and yCoordinate <= upperY:
            resultList.append(line.replace('\n',''))
            
    return resultList

def kwSearchIF(keywords):
    resultList = []
    keywordsExist = True
    for keyword in keywords:
        if keyword in tagsDictionary.keys():
            pass
        else:
            keywordsExist = False
            print("the keyword {} doesn\'t exist in any file".format(keyword))

    if keywordsExist:

        list1 = tagsDictionary.get(keywords[0])
        keywords = keywords[1:len(keywords)]
        
        for keyword in keywords:
            if len(list1) > 0:
                list2 = tagsDictionary.get(keyword)
                if len(list2) > 0:
                    for item in list2:
                        if item in list1:
                            resultList.append(item)
                    list1 = resultList

        return list1
    else:
        list1 = []
        return list1


def kwSpaSearchIF(queryRange,keywords):

    startTime = time.time()
    resultList = kwSearchIF(keywords)
    restaurants = []
    for item in resultList:
        restaurants.append(restaurantsList[int(item)])
    resultList = spaSearchRaw(queryRange,restaurants)
    endTime = time.time()

    print('KwSpaSearchIF: {} results, cost = {} seconds'.format(len(resultList),endTime-startTime))
    for item in resultList:
        print(item)

def kwSpaSearchGrid(queryRange,keywords,lengthX,lengthY,minX,minY):

    startTime = time.time()

    restaurantsToReturn = spaSearchGrid(queryRange,lengthX,lengthY,minX,minY)
    restaurantsList = kwSearchRaw(keywords,restaurantsToReturn)

    endTime = time.time()

    print('kwSearchGrid: {} results, cost = {} seconds'.format(len(restaurantsList),endTime-startTime))
    for restaurant in restaurantsList:
        print(restaurant.replace('\n',''))

def kwSpaSearchRaw(queryRange,keywords):

    startTime = time.time()

    resultListSpaRaw = spaSearchRaw(queryRange,restaurantsList)
    resultListKwRaw = kwSearchRaw(keywords,resultListSpaRaw)


    endTime = time.time()

    print('kwSpaSearchRaw: {} results, cost = {} seconds'.format(len(resultListKwRaw),endTime-startTime))    
    for item in resultListKwRaw:
        print(item)
    

invertedFile = open('invertedFile.tsv')
gridFile = open('gridFile.tsv')
restaurantFile = open('Restaurants_London_England.tsv')
restaurantsList = []

shape = gridFile.readline()
shape = shape.split('\t')
shape[0] = int(shape[0])
shape[1] = int(shape[1])

grid = np.empty(shape,dtype=object)

lengths = gridFile.readline()
lengths = lengths.split('\t')

lengthX = float(lengths[0])
lengthY = float(lengths[1])
minX = float(lengths[2])
minY = float(lengths[3])

for line in restaurantFile:
    restaurantsList.append(line)
    

for line in gridFile:
    lineValues = line.split('\t')
    i = int(lineValues[0])
    j = int(lineValues[1])
    lineValues[2] = lineValues[2].replace('[','')
    value = lineValues[2].replace(']','')
    value = value.replace('\n','')

    if 'None' not in value:
        restaurants = []
        restaurants = value.split(',')
        grid[i][j] = []
        for restaurantId in restaurants:
            grid[i][j].append(int(restaurantId))

tagsDictionary = {}

for line in invertedFile:
    lineValues = line.split('\t')
    tag = lineValues[0]
    lineValues[1] = lineValues[1].replace('\n','')
    fileList = lineValues[1].split(',')
    tagsDictionary[tag] = fileList

lowerX = float(sys.argv[1])
upperX = float(sys.argv[2])
lowerY = float(sys.argv[3])
upperY = float(sys.argv[4])

queryRange = [lowerX,upperX,lowerY,upperY]

keywords = sys.argv[5:len(sys.argv)]

print(queryRange)
print(keywords)

kwSpaSearchIF(queryRange,keywords)
print('')
kwSpaSearchGrid(queryRange,keywords,lengthX,lengthY,minX,minY)
print('')
kwSpaSearchRaw(queryRange,keywords)