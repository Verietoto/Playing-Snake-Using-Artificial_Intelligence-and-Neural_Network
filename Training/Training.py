from Parameters import *
from Snake import Snakes
from Food import Food
from Vector import Vector
from NeuralNetwork import NeuralNetwork

#Chnge Directory Path
os.chdir(sys.path[1])

class GeneticTraining():
    def __init__(self, networkShape, populationNumber, parentNumber, mutationRate):
        self.populaionNumber = populationNumber
        self.shape = networkShape
        self.parentNumber = parentNumber
        self.mutationRate = mutationRate
        self.createPopulation()
        # self.populationFitness = self.calculateFitness(self.population)
        self.update()

    def calculateFitness(self, population):
        populationFitness = []
        cores = multiprocessing.cpu_count()

        fitness1 = Parallel(n_jobs=cores, verbose=1)(delayed(self.runSnakes)(i) for i in population)
        fitness2 = Parallel(n_jobs=cores, verbose=1)(delayed(self.runSnakes)(i) for i in population)
        fitness3 = Parallel(n_jobs=cores, verbose=1)(delayed(self.runSnakes)(i) for i in population)

        for i in range(len(fitness1)):
            populationFitness.append((fitness1[i]+fitness2[i]+fitness3[i])/3)

        return populationFitness

    def createChild(self):
        self.children = []
        parent = list(permutations(self.parent,2))
        np.random.shuffle(parent)

        for i in range(self.parentNumber):
            parent1 = parent[i][0]
            parent2 = parent[i][1]

            child1, child2 = self.crossOver(parent1, parent2)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            self.children.append(child1)
            self.children.append(child2)



    def createPopulation(self):
        self.neuralNetwork = NeuralNetwork(self.shape)
        self.population = []

        for i in range(self.populaionNumber):
            pop = {"Weights": [], "Biases": []}
            pop["Weights"] = self.neuralNetwork.createWeight()
            pop["Biases"] = self.neuralNetwork.createBiasses()
            self.population.append(pop)

    def crossOver(self, parent1Index, parent2Index):
        parent1Weights = self.population[parent1Index]["Weights"]
        parent2Weights = self.population[parent2Index]["Weights"]
        parent1Biases = self.population[parent1Index]["Biases"]
        parent2Biases = self.population[parent2Index]["Biases"]

        child1 = {"Weights": parent1Weights, "Biases": parent1Biases}
        child2 = {"Weights": parent2Weights, "Biases": parent2Biases}


        for i in range(len(parent1Weights)):
            for weighIndex in range(len(child1["Weights"][i])//2):
                if weighIndex%2==0:
                    child1["Weights"][i][weighIndex] = parent1Weights[i][weighIndex]
                    child2["Weights"][i][weighIndex] = parent2Weights[i][weighIndex]

                else:
                    child1["Weights"][i][weighIndex] = parent2Weights[i][weighIndex]
                    child2["Weights"][i][weighIndex] = parent1Weights[i][weighIndex]

            for biasIndex in range(len(child1["Biases"][i])//2):
                if biasIndex%2==0:
                    child1["Biases"][i][biasIndex] = parent1Biases[i][biasIndex]
                    child2["Biases"][i][biasIndex] = parent2Biases[i][biasIndex]
                else:
                    child1["Biases"][i][biasIndex] = parent2Biases[i][biasIndex]
                    child2["Biases"][i][biasIndex] = parent1Biases[i][biasIndex]
        return child1, child2

    def gameOver(self, snake):
        headX = snake.snakeBody[-1][0]
        headY = snake.snakeBody[-1][1]
        if headX < 0 or headX > SCREEN_WIDTH or headY < 0 or headY > SCREEN_HEIGHT or snake.snakeBody[
            -1] in snake.snakeBody[:-1]:
            self.running = False

    def mutation(self, data):
        data = data
        for i in range(len(self.shape)-1):
            for index1, weights in enumerate(data["Weights"][i]):
                for index2, weight in enumerate(weights):
                    random = np.random.randn(1)
                    if random > self.mutationRate:
                        data["Weights"][i][index1][index2] = weight + np.random.randn(1)

            for index1, biases in enumerate(data["Biases"][i]):
                random = np.random.randn(1)
                if random > self.mutationRate:
                    data["Biases"][i][index1] = biases - np.random.rand(1)

        return data

    def update(self):
        generation = 0
        generationThreshold = 10
        savedFitness = [0,0]

        while generation < 100:
            generation +=1
            self.populationFitness = self.calculateFitness(self.population)
            self.parentSelection()
            self.createChild()
            self.childrenFitness = self.calculateFitness(self.children)

            # Append population with child and fitness
            self.population = self.population + self.children
            self.populationFitness = self.populationFitness + self.childrenFitness

            sortingIndex = np.argsort(self.populationFitness)[-self.populaionNumber:]
            self.population = [self.population[idx] for idx in sortingIndex]
            print(np.max(self.populationFitness))
            print(generation)

            # populationSorted = np.argsort(self.populationFitness)
            # bestIndividu = self.population[populationSorted[-1]]
            # bestFitness = self.populationFitness[populationSorted[-1]]
            # savedFitness[0] = bestFitness
            # self.parentSelection()
            # self.createChild()
            # childrenFitness = self.calculateFitness(self.children)
            # print(bestFitness, generation)
            # self.population = self.children
            # self.populationFitness = childrenFitness
            #
            # # for i, j in enumerate(populationSorted[0:len(childrenFitness)]):
            # #     if self.populationFitness[j] < childrenFitness[i]:
            # #         self.population[j] = self.children[i]
            # #         self.populationFitness[j] = childrenFitness[i]
            #
            # generation+=1
            #
            # if savedFitness[1] < savedFitness[0]:
            #     threshold = 10
            #     savedFitness[1] = savedFitness[0]
            # else:
            #     threshold -= 1
            #
            # if threshold == 0:
            #     fivePop = []
            #     fiveFit = []
            #     sorting = np.argsort(self.populationFitness)[-5:]
            #     for i in sorting:
            #         fivePop.append(self.population[i])
            #         fiveFit.append(self.populationFitness[i])
            #     self.createPopulation()
            #     self.populationFitness = self.calculateFitness(self.population)
            #     self.population[0:5] = fivePop
            #     self.populationFitness[0:5] = fiveFit
            #     threshold = 10
            # np.save("Training Result/Weights/Weight_Generation_"+str(generation)+".npy",bestIndividu["Weights"], )
            # np.save("Training Result/Biases/Biases_Generation_" + str(generation) + ".npy", bestIndividu["Biases"])

    def runSnakes(self, individu):
        self.running = True

        snake = Snakes()
        food = Food()
        vector = Vector(snake, food)
        score = 0
        step = 200
        fitness = 0

        while self.running == True:
            self.gameOver(snake)

            if self.running == False or step == 0:
                break

            colision = food.foodCollision(snake)
            if colision == True:
                score +=1
                step += 100
                fitness += 1

            snake.moveBody()
            step -= 1

            input = self.neuralNetwork.feedForward(vector.checkObject(), individu["Weights"],
                                                   individu["Biases"])
            snake.neuralDirection(input)
            fitness += 0.01

        return fitness

    def parentSelection(self):
        fitnessSorted = np.argsort(self.populationFitness)
        self.parent = fitnessSorted[-self.parentNumber:]

        for i in range(self.parentNumber//3):
            random = np.random.randint(0,self.populaionNumber, 1)
            self.parent[self.parentNumber//3 + i] = random


if __name__ == '__main__':
    shape = (24,12,6,3)
    popNumb = 1000
    parentNumber = int(0.3*popNumb)
    mutationRate = 0.2
    algorithm = GeneticTraining(shape, popNumb, parentNumber, mutationRate)
