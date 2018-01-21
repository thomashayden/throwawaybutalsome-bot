from random import *
import time

class markov_chain:

    prob_matrix = None

    def __init__(self, dataArr):
        self.prob_matrix = probability_matrix(dataArr)

    def generate_line(self):
        return self.prob_matrix.generateData()

class probability_matrix:

    lookup_table = []
    prob_matrix = []
    raw_matrix = []

    def __init__(self, dataArr):
        self.parse_data(dataArr)

    def parse_data(self, dataArr):
        self.generateLookupTable(dataArr) # Generates the lookup table for the probability matrix
        self.generateProbabilityMatrix(dataArr) # Generates the actual probability matrix

    def generateLookupTable(self, dataArr):
        self.addToLookupTable("~start") # Add the start tag
        for data in dataArr:
            for word in data:
                self.addToLookupTable(word) # Add each word
        self.addToLookupTable("~end") # Add the end tag

    def addToLookupTable(self, word):
        if(not self.lookup_table.__contains__(word)):
            self.lookup_table.append(word)

    def generateStartingArrayOfSize(self, n):
        arr = []
        for i in range(0, n):
            arr.append(0.0)
        return arr

    def initializeRawandProbMatrix(self):
        self.prob_matrix = []
        self.raw_matrix = []
        for i in range(0, len(self.lookup_table)):
            self.prob_matrix.append(self.generateStartingArrayOfSize(len(self.lookup_table)))
            self.raw_matrix.append(self.generateStartingArrayOfSize(len(self.lookup_table)))

    def generateProbabilityMatrix(self, dataArr):
        self.initializeRawandProbMatrix()

        for data in dataArr:
            self.addDataToProbabilityMatrix(data)

        self.calculateProbabilityMatrix()

    def addDataToProbabilityMatrix(self, data):
        currentWord = "~start"
        nextWord = data[0]
        for i in range(0, len(data)+1):
            self.addWordPairToRawMatrix(currentWord, nextWord)
            currentWord = nextWord
            if i == len(data):
                #print("break")
                break
            elif i == len(data)-1:
                #print("added end tag")
                nextWord = "~end"
            else:
                nextWord = data[i+1]

    def addWordPairToRawMatrix(self, firstWord, nextWord):
        self.raw_matrix[self.lookup_table.index(firstWord)][self.lookup_table.index(nextWord)] += 1

    def calculateProbabilityMatrix(self):
        for coli in range(0, len(self.prob_matrix)):
            sum_of_elements = 0
            for count in self.raw_matrix[coli]:
                sum_of_elements += count
            if sum_of_elements == 0:
                continue
            for rowi in range(0, len(self.prob_matrix[coli])):
                self.prob_matrix[coli][rowi] = self.raw_matrix[coli][rowi] / sum_of_elements

    def generateData(self):
        currentWord = "~start"
        data = ""
        while True:
            time.sleep(0.1)
            nextWord = self.generate_next_word(currentWord)
            #print(nextWord)
            if nextWord == "~end":
                break
            data += " " + nextWord
            currentWord = nextWord
            #print(data)
        return data

    def generate_next_word(self, currentWord):
        current_word_index = self.lookup_table.index(currentWord)
        data = self.prob_matrix[current_word_index]
        #print(data)
        check = 0.0
        for num in data:
            #print(num)
            check += num
        if check > 1.2:
            print("The sum of the parts is signifigantly more than 1! It is: " + str(check) + "! Aborting to " + self.lookup_table[1] + ".")
            return self.lookup_table[1]
        elif check > 1.0 and check <= 1.2:
            print("The sum of the parts is slightly more than 1! It is : " + str(check) + "! Continuing with modified probability.")
            target = random() * check
        elif check < 1.0:
            print("The sum of the parts is less than 1! It is: " + str(check) + "! Continuing with modified probability.")
            target = random() * check
        else:
            target = random()
        current_number = 0.0
        for i in range(0,len(self.prob_matrix[current_word_index])):
            added_prob = self.prob_matrix[current_word_index][i]
            if target >= current_number and target < current_number + added_prob:
                return self.lookup_table[i]
            current_number += added_prob
        print("No word was found for some reason. current_number is " + str(current_number) + ". Aborting to " + self.lookup_table[1] + ".")
        return self.lookup_table[1]

#pm = probability_matrix(
#        ["This is some sample data I am playing with".split(),
#         "The sample data is intended to provide insight into the program".split(), "You really need a lot of data to make the program work".split(),
#         "I am just typing a lot into here to try and get it to make something interesting".split(), "It is important to have similar but unique information for the program to work with".split(),
#         "This includes data that contains the same words for the program to mix and match".split()])
# print(pm.lookup_table)
#
# for i in pm.raw_matrix:
#     print(i)
#
# time.sleep(0.3);
# print("====================")
#
# for i in pm.prob_matrix:
#     print(i)
#
# time.sleep(1);

#print(pm.generateData())