"""Setting up weight and bias update using genetic algorithm"""
from Parameters import *
from Snake import Snakes
from Food import Food
from Vector import Vector
from NeuralNetwork import NeuralNetwork
from Arena import  Arena

#Chnge Directory Path
"""Because i put this py not in root folder so i change main directory to root directory"""
os.chdir(sys.path[1])

class TraingSnake():
    def __init__(self, networkShape, populationNumber, parentNumber, mutationRate):
        """

        :param networkShape: Shape of neural network. See in parameters (shape0,shape1,shape2)
        :param populationNumber: integer of how many population made (int(number))
        :param parentNumber: how many in population will take a breed (int(number)
        :param mutationRate:Rate of mutation in genome (float(nunver))
        """
        self.populationNumber = populationNumber
        self.shape = networkShape
        self.parentNumber = parentNumber
        self.mutationRate = mutationRate
        self.brain = NeuralNetwork(self.shape)
        self.update()

    def calculateFitness(self, population, display=False):
        """
        calculate fitness of a set of individu. each individu will be played 3 times
        :param population: [[individu1],....,[individu_N]]
        :param display: if true we will see the progress
        :return:
        """
        populationFitness = []

        for i in range(len(population)):
            if display == True:
                sys.stdout.write('\r'+"Progress: "+str(100*(i+1)/len(population)))
                sys.stdout.flush()
            score1 = self.runSnakes(population[i])
            score2 = self.runSnakes(population[i])
            score3 = self.runSnakes(population[i])
            score = float("{0:.4f}".format((score1+score2+score3)/3))
            populationFitness.append(score)
        return populationFitness

    def createChild(self):
        """
        using 2 crossover method and only pick the best one to append as children
        children = list([children1],....,[childrenN])
        :return:
        """
        self.children = []
        self.childrenFitnesss = []
        parent = list(permutations(self.parents, 2))
        np.random.shuffle(parent)
        maxChild = 0
        sys.stdout.write('\n')
        sys.stdout.flush()
        for i in range(self.populationNumber):
            sys.stdout.write('\r' + "Progress Children: " + str(100 * (i+1) / self.populationNumber)+ "\t"+
                             "maximum Children Fitness: " + str(maxChild))
            sys.stdout.flush()
            parent1 = parent[i][0]
            parent2 = parent[i][1]
            child1, child2 = self.crossOver(parent1, parent2)
            child3, child4 = self.crossOver2(parent1,parent2)
            popChild = [self.mutation(child1),self.mutation(child2),self.mutation(child3),self.mutation(child4)]
            fitChild = self.calculateFitness(popChild)
            winner = popChild[np.argmax(fitChild)]
            self.children.append(winner)
            self.childrenFitnesss.append(max(fitChild))
            if max(fitChild) > maxChild:
                maxChild = max(fitChild)

    def createPopulation(self):
        "Create initial Population"
        self.neuralNetwork = NeuralNetwork(self.shape)
        self.population = []
        for i in range(self.populationNumber):
            weights = self.neuralNetwork.createWeight()
            biases = self.neuralNetwork.createBiasses()
            self.population.append([weights, biases])

    def crossOver(self, parent1, parent2):
        """Cross over using method 1, weight and bias are converted into 8 bit binary then swipe weight1 and weight2
        on certain offspring
        :return new 2 individu"""
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)

        #Weights Cross Over
        for index1 in range(len(child1[0])):
            for index2 in range(len(child1[0][index1])):
                random = np.random.rand()
                for index3 in range(len(child1[0][index1][index2])):
                    if random < 0.5:
                        bin1 = floatToBinary(child1[0][index1][index2][index3])
                        bin2 = floatToBinary(child2[0][index1][index2][index3])

                        child2[0][index1][index2][index3] = binaryToFloat(bin2[0:4] + bin1[4:])
                        child1[0][index1][index2][index3] = binaryToFloat(bin1[0:4] + bin2[4:])
                    else:
                        u = np.random.rand()
                        if u <= 0.5:
                            beta = pow(2*u, 1/(51))
                        else:
                            beta = pow(1/(2*u-1), 1/(51))

                        child1[0][index1][index2][index3] = 0.5*((1+beta)*parent1[0][index1][index2][index3] + (1-beta)*parent2[0][index1][index2][index3])
                        child2[0][index1][index2][index3] = 0.5 * ((1 + beta) * parent2[0][index1][index2][index3] + (1 - beta) *parent1[0][index1][index2][index3])

        #Biases Cross Over
        for index1 in range(len(child1[1])):
                child1[1][index1] = 0.7*parent1[1][index1] + 0.3*parent2[1][index1]
                child2[1][index1] = 0.2*parent1[1][index1] + 0.8*parent2[1][index1]
        return child1, child2

    def crossOver2(self, parent1, parent2):
        """Cross over type 2 is on;ly swipe neuron in a layer or making a sum of percentage*weight1 + percentage2*weight2
        where percentage1+percentage2 must equal to 1
        :return 2 new Individu
        """
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)

        #Weights Cross Over
        for index1 in range(len(child1[0])):
            for index2 in range(len(child1[0][index1])):
                lenIndex2 = len(parent1[0][index1][index2])//2
                child1[0][index1][index2][-lenIndex2:] = parent2[0][index1][index2][-lenIndex2:]
                child2[0][index1][index2][-lenIndex2:] = parent1[0][index1][index2][-lenIndex2:]

        #Biases Cross Over
        for index1 in range(len(child1[1])):
                child1[1][index1] = 0.7*parent1[1][index1] + 0.3*parent2[1][index1]
                child2[1][index1] = 0.2*parent1[1][index1] + 0.8*parent2[1][index1]
        return child1, child2

    def gameOverCheck(self, snake):
        """
        check if snake hit the wall or body
        :param snake:
        :return:  True if colllides, false if not collides
        """
        gameOver = False
        headX = snake.snakeBody[-1][0]
        headY = snake.snakeBody[-1][1]

        if headX < 0:
            gameOver = True
            print("Collides with left Wall")
        elif headY < 0:
            gameOver = True
            print("Collides with lower wall")
        elif headX >= SCREEN_WIDTH:
            gameOver = True
            print("Collides with right wall")
        elif headY >= SCREEN_HEIGHT:
            gameOver = True
            print("Collides with upper wall")
        elif snake.snakeBody[-1] in snake.snakeBody[:-1]:
            gameOver = True
            print("Collides with body")

        return gameOver

    def mutation(self,individu):
        """
        Mutate Individu
        :param individu: list([Weights],[Biases])
        :return: mutated individu: list([Weights],[Biases])
        """
        mutated = np.array(copy.deepcopy(individu))

        #Weight Mutation
        weights = mutated[0]
        biases = mutated[1]

        #Weights mutation
        for index1, weights1 in enumerate(weights):
            for index2, weights2 in enumerate(weights1):
                for index3, weights3 in enumerate(weights2):
                    random = np.random.rand(1)
                    if random < self.mutationRate:
                        mutated[0][index1][index2][index3] = np.random.randn()
        for index1, bias1 in enumerate(biases):
            for index2, bias2 in enumerate(bias1):
                random = np.random.rand(1)
                if random < self.mutationRate:
                    mutated[1][index1][index2] = np.random.randn()
        return mutated

    def runSnakes(self,individu, display=False):
        """
        Running snake. Individu point is 1000*Score + Age
        :param individu: list([weight],[biases])
        :param display: if True snake game will displayed)
        :return: Score or Fotness
        """
        running = True
        snake = Snakes()
        food = Food()
        score = 0
        age = 0
        remainStep = 200

        if display == True:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            surface = pygame.Surface(screen.get_size())
            surface = surface.convert()
            clock = pygame.time.Clock()


        while running == True:
            vector = Vector(snake,food)
            input = vector.checkObject()
            feedForward = self.brain.feedForward(input, individu[0], individu[1])
            snake.neuralDirection(feedForward)
            snake.moveBody()

            gameOver = self.gameOverCheck(snake)
            if gameOver == True or remainStep == 0:
                running = False

            grow, snake.snakeBody = food.foodCollision(snake)
            if grow == True:
                score += 1
                remainStep += 100

            age += 1
            remainStep -= 1

            if display == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.runing = False
                        pygame.quit()
                Arena(gridsize=GRID_SIZE, screen=surface)
                snake.drawBody(surface)
                food.draw(surface)
                screen.blit(surface, (0, 0))
                pygame.display.update()
                clock.tick(20)

        return 1000*score + age

    def selectParent(self):
        """
        Choosing parent to breed. There is 2 ways:
        1. using roullete choice based on fitness then mutate parent1 so we get 2 parents
        2. Pick best parent based on fitness itself
        after that we re-calculate fitness then pick ParentNumber best parents to breed

        :return: self.parent (set of individu)
        """
        popIndex = np.arange(0, len(self.population), 1)
        probability = np.array(self.populationFitness.copy())
        probability = probability/sum(probability)

        self.parents = []
        randomIndex = np.random.choice(popIndex, self.parentNumber, replace=False, p=probability)
        parent1 = [self.population[parent] for parent in randomIndex]
        parent2 = [self.mutation(self.population[parent]) for parent in randomIndex]
        self.parents = parent1+parent2

        print("===============Parent Progress==============")
        self.parentsFitness = self.calculateFitness(self.parents, display=True)
        sortedIndex = np.argsort(self.parentsFitness)[-self.parentNumber:]
        self.parents = [self.parents[index] for index in sortedIndex]
        self.parentsFitness = [self.parentsFitness[index] for index in sortedIndex]

        print("\tBeast Parent Fitness:" + str(max(self.parentsFitness)))

    def update(self):
        """
        Update weight and biases each individu every generation
        :return:
        """
        self.createPopulation()
        self.populationFitness = self.calculateFitness(self.population, display=True)
        generation = 0

        while generation < 1000:
            print("\nGeneration: " + str(generation))
            self.selectParent()
            self.createChild()
            self.population = self.population + self.parents + self.children
            self.populationFitness = self.populationFitness + self.parentsFitness + self.childrenFitnesss

            # Soering
            popSorting = np.argsort(self.populationFitness)[-self.populationNumber:]
            popSorting = popSorting[::-1]
            self.population = [self.population[x] for x in popSorting]
            self.populationFitness = [self.populationFitness[x] for x in popSorting]

            generation += 1
            np.save("Training Result/Test/Training_" + str(generation) + "_" + str(self.populationFitness[0]) + ".npy",
                    self.population[0])
            self.runSnakes(self.population[0], display=True)
            print('\n top 6 Best Fitness: ' + str(self.populationFitness[0:6]))
            print('\n Lowest 6 Fitness: ' + str(self.populationFitness[-6:]))
            print("Population Length:"+str(len(self.population)))



def floatToBinary(number):
    number = float("{0:.4f}".format(number))
    bit = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    if number < 0:
        bit[0] = 1
        number = abs(number)
    for i in range(1, 9):
        number *= 2
        if number > 1:
            bit[i] = 1
            number = -int(number) + number
        elif number < 1:
            bit[i] = 0
        elif number == 0:
            break
    return bit

def binaryToFloat(binaryList):
    num = 0
    for i in range(1, 9):
        num += binaryList[i] * pow(2, -i)
    if binaryList[0] == 1:
        num *= -1
    num = float("{0:.4f}".format(num))
    return num

if __name__ == '__main__':
    algorithm = TraingSnake(shape, popNumb, parentNumber, mutationRate)