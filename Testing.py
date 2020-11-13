"""
Test Trained Snakes
"""
from Parameters import *
from Snake import Snakes
from Food import Food
from Vector import Vector
from NeuralNetwork import NeuralNetwork
from Arena import Arena

class main():
    def __init__(self):
        """
        self.load and self.testing is only test 1 individu with highest score or the choosen one
        self.runPop is running all trained snakes
        """
        self.generation = 0
        self.best = 0
        self.brain = NeuralNetwork(shape)
        self.load()
        self.testing()
        # self.runPop()

    def runPop(self):
        """
        Fill basepath of your trained snake's weights and biases saved
        :return:
        """
        basepath = 'Training Result/Test'

        file = []
        for entry in os.listdir(basepath):
            if entry.endswith(".npy"):
                file.append(entry.split("_"))
        score = [int(scores[1]) for scores in file]
        self.file = [file[x] for x in np.argsort(score)]
        for i in range(len(self.file)):
            loaded = np.load(basepath+"/"+"_".join(self.file[i]))
            score = self.runSnakes(loaded, display=True)
            self.generation += 1
            if score > self.best:
                self.best = score
    def load(self):
        """
        Change k for pick Nth Best snake trained
        :return:
        """
        # basepath = 'Training Result/Test2'
        # basepath = 'Training Result/Test'
        file = []
        for entry in os.listdir(basepath):
            if entry.endswith(".npy"):
                file.append(entry.split("_"))
        score = [float(scores[-1].split(".npy")[0]) for scores in file]
        index = np.argsort(score)[::-1]
        file = [file[x] for x in index]
        k=0
        self.test = np.load(basepath+"/"+'_'.join(file[k]))
        print(file[k])

    def testing(self):
        score = self.runSnakes(self.test, display=True)
        print(score)
    def gameOverCheck(self, snake):
        gameOver = False
        headX = snake.snakeBody[-1][0]
        headY = snake.snakeBody[-1][1]
        if headX < 0:
            gameOver = True
        elif headY < 0:
            gameOver = True
        elif headX >= SCREEN_WIDTH:
            gameOver = True
        elif headY >= SCREEN_HEIGHT:
            gameOver = True
        elif snake.snakeBody[-1] in snake.snakeBody[:-1]:
            gameOver = True

        return gameOver

    def runSnakes(self,individu, display=False):

        running = True
        snake = Snakes()
        food = Food()
        score = 0
        age = 0
        remainStep = 300

        if display == True:
            screens = pygame.display.set_mode((SCREEN_WIDTH+400, SCREEN_HEIGHT))
            surface = pygame.Surface(screens.get_size())
            surface = surface.convert()
            clock = pygame.time.Clock()


        while running == True:
            vector = Vector(snake, food)
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
                remainStep += 200

            age += 1
            remainStep -= 1

            if display == True:
                Arena(gridsize=GRID_SIZE, screen=surface)
                snake.drawBody(surface)
                food.draw(surface)
                screens.blit(surface, (0, 0))
                Arena.drawNeuralNetwork(screens, input, individu, feedForward)
                Arena.drawScore(screens,score,self.best,self.generation)
                pygame.display.update()
                clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runing = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    snake.changeDirection(event.key)

        return score


if __name__ == '__main__':
    main()