#Stefanos Galanis 2032
import sys
import time

def exportInvertedFile(orderedFrequencies):

    exportedFile = open('invertedFile.tsv','w')

    for key in tagsDictionary.keys():
        output = '' + key +'\t'
        fileList = tagsDictionary[key]
        iteration = 1
        for filedId in fileList:
            if iteration == 1:
                output += str(filedId)
                iteration += 1
            else:
                output += ',' + str(filedId)
        output += '\n'    
        exportedFile.write(output)

def kwSearchRaw(keywords):

    startTime = time.time()

    restaurantFile = open('Restaurants_London_England.tsv')
    restaurantsList = []

    for line in restaurantFile:
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
        endTime = time.time()
        totalExecutionTime = endTime - startTime
        print('kwSearchRaw: {} results, cost = {} seconds'.format(len(restaurantsList),totalExecutionTime))
        for restaurant in restaurantsList:
            print(restaurant.replace('\n',''))
    else:
        endTime = time.time()
        totalExecutionTime = endTime - startTime
        print('kwSearchRaw: {} results, cost = {} seconds'.format(len(restaurantsList),totalExecutionTime))
        #print('no matches for these keywords')

def kwSearchIF(keywords):
    startTime = time.time()
    resultList = []
    keywordsExist = True
    for keyword in keywords:
        if keyword in tagsDictionary.keys():
            pass
        else:
            keywordsExist = False
            print("the keyword {} doesn\'t exist in any file".format(keyword))

    if keywordsExist:

        print(keywords)
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

        endTime = time.time()
        totalExecutionTime = endTime - startTime
        print('kwSearchIF: {} results, cost = {} seconds'.format(len(list1),totalExecutionTime))
        for storeId in list1:
            print(restaurantsList[int(storeId)].replace('\n',''))
        #print("total time for invertedFile search :{} seconds \nand the results that matched the keyword: {}".format((endTime-startTime),list1))
    else:
        endTime = time.time()
        totalExecutionTime = endTime - startTime
        print('kwSearchIF: {} results, cost = {} seconds'.format(len(list1),totalExecutionTime))
        #print("total time for invertedFile search :{} seconds \nwe found no results".format((endTime-startTime)))
    

restaurantFile = open('Restaurants_London_England.tsv')
tagsDictionary = {}
numberOfLine = 0
restaurantsList = []
frequenciesDictionary = {}
#stopWordsList = [' & ',' and ',' ','.','/']

for line in restaurantFile:
    lineValues = line.split('\t')
    restaurantsList.append(line)
    fileName = lineValues[0]
    coordinates = lineValues[1]
    tags = lineValues[2]

    tagsLength = len(tags)
    tags = tags[6:tagsLength-1].split(',')

    for tag in tags:
        if tag in tagsDictionary.keys():

            frequency = frequenciesDictionary.get(tag)
            frequency += 1
            frequenciesDictionary[tag] = frequency

            tagValue = tagsDictionary.get(tag)
            tagValue.append(str(numberOfLine))
            tagsDictionary[tag] = tagValue
            tagValue = []
        else:
            frequency = 1
            frequenciesDictionary[tag] = frequency

            tempList = [str(numberOfLine)]
            tagsDictionary[tag] = tempList

    numberOfLine += 1

restaurantFile.close()

orderedFrequencies = {k: v for k, v in sorted(frequenciesDictionary.items(), key=lambda item: item[1])}
print(orderedFrequencies.values())

exportInvertedFile(orderedFrequencies)

keywords = sys.argv[1:len(sys.argv)]

kwSearchIF(keywords)

kwSearchRaw(keywords)


