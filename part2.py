#Stefanos Galanis 2032
import sys
import time
import heapq
import numpy as np

def exportGridAsFile(grid,lenghtX,lengthY,minX,minY):
    print(grid.shape)
    exportedFile = open('gridFile.tsv','w')

    header = '{}\t{}\n'.format(grid.shape[0],grid.shape[1])
    exportedFile.write(header)
    subHeader = '{}\t{}\t{}\t{}\n'.format(lenghtX,lengthY,minX,minY)
    exportedFile.write(subHeader)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            output = '{}\t{}\t{}\n'.format(i,j,grid[i][j])
            exportedFile.write(output)

def spaSearchRaw(lowerX,upperX,lowerY,upperY):
    restaurantFile = open('Restaurants_London_England.tsv')
    numberOfResultsRaw = 0
    resultList = []

    startTime = time.time()

    for line in restaurantFile:
        lineValues = line.split('\t')
        coordinates = lineValues[1]
        coordinates = coordinates[9:len(coordinates)]
        coordinates = coordinates.strip().split(',')


        xCoordinate = float(coordinates[0])
        yCoordinate = float(coordinates[1])
        
        if xCoordinate >= lowerX and xCoordinate <= upperX and yCoordinate >= lowerY and yCoordinate <= upperY:
            resultList.append(line.replace('\n',''))
            numberOfResultsRaw += 1

    endTime = time.time()

    totalExecutionTime = endTime - startTime

    print('spaSearchRaw: {} results, cost = {} seconds'.format(numberOfResultsRaw,totalExecutionTime))
    for item in resultList:
        print(item)
    print('spaSearchRaw: {} results, cost = {} seconds'.format(numberOfResultsRaw,totalExecutionTime))


xCoordinateList = []
yCoordinateList = []


restaurantFile = open('Restaurants_London_England.tsv')
restaurantsList = []

for line in restaurantFile:
    restaurantsList.append(line)
    lineValues = line.split('\t')
    coordinates = lineValues[1]
    coordinates = coordinates[9:len(coordinates)]
    coordinates = coordinates.strip().split(',')

    #print(coordinates)
    xCoordinateList.append(float(coordinates[0]))
    yCoordinateList.append(float(coordinates[1]))

restaurantFile.close()

xCoordinateList.sort()
yCoordinateList.sort()

minX = xCoordinateList[0]
minY = yCoordinateList[0]
maxX = xCoordinateList[-1]
maxY = yCoordinateList[-1]

print('max X :{} min X :{} max Y :{} min Y :{} '.format(maxX,minX,maxY,minY))
print('bounds: {} {} {} {} '.format(maxX,minX,maxY,minY))


lenghtX = maxX - minX
lengthY = maxY - minY

print('widths: {} {}'.format(lenghtX,lengthY))

fragSizeX = lenghtX / 50
fragSizeY = lengthY / 50

print('fragment size on x(axis): {} fragment size on y(axis): {}'.format(fragSizeX,fragSizeY))
border1 = minX
border2 = minX
for i in range(0,50):
    if i == 0 :
        pass
    else:
        border1 += fragSizeX
    border2 += fragSizeX 
    print('{} {}-{}'.format(i,border1,border2))

grid = np.empty(shape=(50,50),dtype=object)
numberOfLine = 0

restaurantFile = open('Restaurants_London_England.tsv')

for line in restaurantFile:
    lineValues = line.split('\t')
    coordinates = lineValues[1]
    coordinates = coordinates[9:len(coordinates)]
    coordinates = coordinates.strip().split(',')

    locationX = float(coordinates[0])
    locationY = float(coordinates[1])

    distX = locationX - minX
    distY = locationY - minY

    distXinBlocks = int(distX/fragSizeX)
    distYinBlocks = int(distY/fragSizeY)

    if distXinBlocks == 50 :
        distXinBlocks -= 1
    if distYinBlocks == 50 :
        distYinBlocks -= 1

    

    if grid[distXinBlocks][distYinBlocks] == None: 
        grid[distXinBlocks][distYinBlocks] = [numberOfLine]
    else:
        grid[distXinBlocks][distYinBlocks].append(numberOfLine)

    

    numberOfLine += 1

numberOfNonEmptyBlocks = 0



for i in range(0,50):
    for j in range(0,50):
        if grid[i][j] != None:
            numberOfNonEmptyBlocks += 1
            print('block[{}][{}]:{}'.format(i,j,len(grid[i][j])))#arithmo thelei

lowerX = float(sys.argv[1])
upperX = float(sys.argv[2])
lowerY = float(sys.argv[3])
upperY = float(sys.argv[4])


lowerBoundX = float(sys.argv[1]) - minX
upperBoundX = float(sys.argv[2]) - minX
lowerBoundY = float(sys.argv[3]) - minY
upperBoundY = float(sys.argv[4]) - minY

upperBoundX = int(upperBoundX/fragSizeX)
lowerBoundX = int(lowerBoundX/fragSizeX)
upperBoundY = int(upperBoundY/fragSizeY)
lowerBoundY = int(lowerBoundY/fragSizeY)

if upperBoundX == 50:
    upperBoundX -= 1
if lowerBoundX == 50:
    lowerBoundX -= 1
if upperBoundY == 50:
    upperBoundY -= 1
if lowerBoundY == 50:
    lowerBoundY -= 1




startTime = time.time()
restaurantsToRetrieve = []
additive = 0
print(lowerBoundX,upperBoundX,lowerBoundY,upperBoundY)


counter = 0
for i in range(lowerBoundX,upperBoundX+1):
    for j in range(lowerBoundY,upperBoundY+1):
        print(i,j)
        if grid[i][j] != None:
            restaurants = grid[i][j]
            additive += len(restaurants)
            for restaurantID in restaurants:
                restaurantsToRetrieve.append(int(restaurantID))

resultListGrid = []
numberOfResultsGrid = 0

for restaurant in restaurantsToRetrieve:
    line = restaurantsList[restaurant]
    lineValues = line.split('\t')
    coordinates = lineValues[1]
    coordinates = coordinates[9:len(coordinates)]
    coordinates = coordinates.strip().split(',')

    xCoordinate = float(coordinates[0])
    yCoordinate = float(coordinates[1])

    if xCoordinate >= lowerX and xCoordinate <= upperX and yCoordinate >= lowerY and yCoordinate <= upperY:
            resultListGrid.append(line.replace('\n',''))



endTime = time.time()

totalExecutionTime = endTime-startTime

spaSearchRaw(lowerX,upperX,lowerY,upperY)

print('spaSearchGrid: {} results, cost = {} seconds'.format(len(resultListGrid),float(totalExecutionTime)))
for restaurant in resultListGrid:
    print(restaurant)

exportGridAsFile(grid,lenghtX,lengthY,minX,minY)
