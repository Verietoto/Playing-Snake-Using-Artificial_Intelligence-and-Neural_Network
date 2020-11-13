"""
This Code Controll The Arena Arena
"""

from Parameters import *

class Arena():
    def __init__(self, gridsize, screen):
        """

        :param gridsize: is how big the grid (rectangel). Find setting in Parameters.py
        :param screen: Which Screen i want to show the arena
        """
        self.gridSize = gridsize
        self.screen = screen
        self.direction = [UP,DOWN, RIGHT, LEFT]
        self.createGrid()
        self.drawLogo()

    def drawLogo(self):
        """
        Drawing my logo just in case someone want stole my video
        :return:
        """
        logo = pygame.image.load("Pictures/Logo.png")
        logo = pygame.transform.scale(logo, (5*GRID_SIZE,5*GRID_SIZE))
        self.screen.blit(logo, (SCREEN_WIDTH+SCREEN_WIDTH2-50,30))

    def createGrid(self):
        """
        Create Arena Visualization. With grid like chess board
        You can change the color in parameters for color1 and color2
        :return:
        """
        for x in range(int(SCREEN_WIDTH/self.gridSize)):
            for y in range(int(SCREEN_HEIGHT/self.gridSize)):
                if (x+y)%2 == 0:
                    r = pygame.Rect((x*self.gridSize, y*self.gridSize), (self.gridSize,self.gridSize))
                    pygame.draw.rect(self.screen, GRID_COLOR_1, r)
                else:
                    rr = pygame.Rect((x*self.gridSize, y*self.gridSize), (self.gridSize,self.gridSize))
                    pygame.draw.rect(self.screen, GRID_COLOR_2, rr)

    def drawScore(screen,score,best, gen):
        """
        Drawing Socre when testing
        :param score: integer
        :param best: integer
        :param gen: integer
        :return:
        """
        pygame.font.init()
        font = pygame.font.Font('freesansbold.ttf', 20)

        bestImage = pygame.image.load("Pictures/Throphy.png")
        scoreImage = pygame.image.load("Pictures/Tomatos.png")
        scoreText = font.render("X"+str(score), True, (255, 255, 255))
        bestText = font.render("X" + str(best), True, (255, 255, 255))
        genText = font.render("Gen: " + str(gen), True, (255, 255, 255))
        screen.blit(genText, (SCREEN_WIDTH + SCREEN_WIDTH2 - 40, SCREEN_HEIGHT - 30))
        screen.blit(scoreText, (SCREEN_WIDTH + 170, SCREEN_HEIGHT-30))
        screen.blit(bestText, (SCREEN_WIDTH + 70, SCREEN_HEIGHT - 30))
        screen.blit(bestImage, (SCREEN_WIDTH+40,SCREEN_HEIGHT-40))
        screen.blit(scoreImage, (SCREEN_WIDTH+140,SCREEN_HEIGHT-40))


    def drawNeuralNetwork(screen, input,  weights, output):
        """
        Vizualising neural network. by changing the array into percentage i can controll circle opacity

        :param input: Input is 24 vector of snakes looking for wall, food, dan snake body (array)
        :param weights: input is weights and biases (array with size [[Weights],[Biases]]
        :param Output is feedforward result to define direction
        :return:
        """
        pygame.font.init()
        font = pygame.font.Font('freesansbold.ttf', 13)
        dirList = ["UP", "RIGHT", "DOWN", "LEFT"]
        input = np.array(input).reshape(-1)
        input = 255*(input-np.min(input))/(np.max(input)-np.min(input)) if sum(input) !=0 else [0 for _ in range(24)]
        top5 = np.argsort(input)[-5:]
        pygame.font.init()


        stepY = 22
        stepX = 60
        #Draw Neuron
        for i in range(len(shape)):
            for j in range(shape[i]):
                y = int((SCREEN_HEIGHT-shape[i]*stepY)/2) + stepY*j
                x = 20 + SCREEN_WIDTH + i*stepX

                pygame.gfxdraw.filled_circle(screen, x, y, 7, (255,255,255))  # draw neuron
                if i == 0:
                    """Draw Basic Circle"""
                    pygame.gfxdraw.filled_circle(screen, x, y, 7, (124, 253, 0, input[j]))

                elif i == 1:
                    if j in top5:
                        """Draw first layer Green Circle"""
                        input = np.array(weights[0][0][j]).reshape(-1)
                        input = 255 * (input - np.min(input)) / (np.max(input) - np.min(input))
                        pygame.gfxdraw.filled_circle(screen, x, y, 7, (124, 153, 25, input[j]))

                if i < len(shape) - 1:
                    """Draw Lines"""
                    for z in range(shape[i + 1]):
                        if z % 3 == 0:
                            x2 = 30 + SCREEN_WIDTH + (i + 1) * stepX
                            y2 = int((SCREEN_HEIGHT - shape[i + 1] * stepY) / 2) + stepY * z
                            pygame.gfxdraw.line(screen, x, y, x2, y2, (255, 0, 25, 40))
                        else:
                            x2 = 20 + SCREEN_WIDTH + (i + 1) * stepX
                            y2 = int((SCREEN_HEIGHT - shape[i + 1] * stepY) / 2) + stepY * z
                            pygame.gfxdraw.line(screen, x, y, x2, y2, (0, 255, 155, 40))
                if i == 3:
                    """Draw Output Teks and Green Circle indating direction"""
                    directionText = font.render(dirList[j], True, (255, 255, 255))
                    screen.blit(directionText, (x+20,y))
                    if j == np.argmax(output):
                        pygame.gfxdraw.filled_circle(screen, x, y, 7, (125, 253, 25, 255))









