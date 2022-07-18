import random


# Globals
generation = 1
GlobalMaxValueIDX = None
isAllOne = False
populationTable = [[None for i in range(3)] for i in range(25)]


def findMaxFitness(ptable):
    tempList = []
    for i in range(len(ptable)):
        tempList.append(int(ptable[i][2]))
    currentMax = max(tempList)
    for i in range(len(ptable)):
        if currentMax == ptable[i][2]:
            return i

# Generating population


def startProgram():
    global GlobalMaxValueIDX, populationTable, generation

    for i in range(25):
        randomValue = random.randint(1, 4294967295)
        populationTable[i][0] = randomValue
        convertedBinary = "{:032b}".format(randomValue)
        convertedBinary = str(convertedBinary)
        populationTable[i][1] = (str(convertedBinary))
        fitnessValue = 0
        for char in convertedBinary:
            if char == "1":
                fitnessValue += 1
        populationTable[i][2] = (fitnessValue)

    GlobalMaxValueIDX = findMaxFitness(populationTable)
    ShowCurrentGen(populationTable)
    print("Generation %i best individual fitness is %i \n" %
          (generation, populationTable[GlobalMaxValueIDX][2]))


def fitnessValue(convertedBinary):
    fitnessVal = 0
    for char in convertedBinary:
        if char == "1":
            fitnessVal += 1
    return fitnessVal


def generateNewPopulation():
    populationTable = [[None for i in range(3)] for i in range(25)]
    return populationTable


def ShowCurrentGen(currentPopulationTable):
    for i in range(len(currentPopulationTable)):
        print("individual %i : [%s] and fitness is %i" % (
            i+1, currentPopulationTable[i][1], currentPopulationTable[i][2]))


def crossover(populationTable, currentPopulationTable, tempValueIDX, maxValueIDX, currentIDX):
    # casting problems?
    x1 = [x for x in populationTable[tempValueIDX][1]]
    x2 = [x for x in populationTable[maxValueIDX][1]]
    x1_offspring = []
    x2_offspring = []

    for i in range(0, 32):
        # if 16 it means half
        if i == 16:
            x1_offspring.append(str(x2[i]))
            x2_offspring.append(str(x1[i]))

        else:
            x1_offspring.append(str(x1[i]))
            x2_offspring.append(str(x2[i]))

    x1_offspring = "".join(x1_offspring)
    x2_offspring = "".join(x2_offspring)
    currentPopulationTable[currentIDX][1] = x1_offspring
    currentPopulationTable[currentIDX+1][1] = x2_offspring

    currentPopulationTable[currentIDX][0] = int(x1_offspring, 2)
    currentPopulationTable[currentIDX+1][0] = int(x2_offspring, 2)
    currentPopulationTable[currentIDX][2] = fitnessValue(x1_offspring)
    currentPopulationTable[currentIDX+1][2] = fitnessValue(x2_offspring)

    return currentPopulationTable


def Mutation(populationTable, currentPopulationTable, tempValueIDX, MutateCurrentChoice, currentIDX):
    if MutateCurrentChoice == "NoMutate":
        return currentPopulationTable
    currentBinaryArray = [str(x) for x in populationTable[tempValueIDX][1]]
    randomGene = random.randint(0, 31)
    if currentBinaryArray[randomGene] == "1":
        currentBinaryArray[randomGene] = "0"
    else:
        currentBinaryArray[randomGene] = "1"

    currentBinaryString = ("").join(currentBinaryArray)
    currentPopulationTable[currentIDX][1] = currentBinaryString
    currentPopulationTable[currentIDX][0] = int(currentBinaryString, 2)
    currentPopulationTable[currentIDX][2] = fitnessValue(currentBinaryString)

    return currentPopulationTable


def main():
    global isAllOne, GlobalMaxValueIDX, populationTable, generation
    startProgram()
    while(isAllOne == False):
        currentPopulationTable = generateNewPopulation()
        currentValue = 0
        # filing new population
        while(currentValue < 25):
            # creating choices
            choices = ["selection", "mutation"]
            currentChoice = random.choices(choices, weights=(50, 50), k=1)
            tempValueIDX = None

            # prepping for selection
            while True:
                tempValueIDX = random.randint(0, 24)
                if tempValueIDX != GlobalMaxValueIDX:
                    break
                
            if currentChoice[0] == "selection" and currentValue <= 23:
                #protecting incase there is a bad mutation
                while(currentPopulationTable[currentValue][0] is None or currentPopulationTable[currentValue][1] is None or currentPopulationTable[currentValue][2] is None) or (currentPopulationTable[currentValue+1][2] is None or currentPopulationTable[currentValue+1][0] is None or currentPopulationTable[currentValue+1][1] is None):
                    tempPopulationTable = crossover(
                        populationTable, currentPopulationTable, tempValueIDX, GlobalMaxValueIDX, currentValue)
                    currentPopulationTable = tempPopulationTable
                currentValue += 2

            else:
                MutateChoices = ["Mutate", "NoMutate"]
                #protecting incase there is a bad mutation
                while(currentPopulationTable[currentValue][0] is None or currentPopulationTable[currentValue][1] is None or currentPopulationTable[currentValue][2] is None):
                    MutateCurrentChoice = random.choices(
                        MutateChoices, weights=(99, 1), k=1)
                    tempPopulationTable = Mutation(
                        populationTable, currentPopulationTable, tempValueIDX, MutateCurrentChoice[0], currentValue)
                    currentPopulationTable = tempPopulationTable
                currentValue += 1

        # Updating population using offsprings
        populationTable = currentPopulationTable
        # adding generation
        generation += 1

        # Checking if we have reached the optimum criteria
        TopFitnessValueIDX = findMaxFitness(populationTable)

        #Updating the value 
        GlobalMaxValueIDX = TopFitnessValueIDX

        #Printing the chromosomes and fitness value
        ShowCurrentGen(currentPopulationTable)
        print("Generation %i best individual fitness is %i \n" %
              (generation, populationTable[TopFitnessValueIDX][2]))
        
        # Checker for optimum
        if populationTable[TopFitnessValueIDX][2] == 32:
            isAllOne = True
            break


main()
