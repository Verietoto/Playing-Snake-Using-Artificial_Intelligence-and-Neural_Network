""" This py controll everything about snake
initial position
drawing body
turn snake's direction
Moving body
"""
from Parameters import *

class Snakes():
    def __init__(self):
        """Only setting up for initial dorevtion and initial position"""
        self.snakeBody = [(100, 100), (120, 100), (140, 100)]
        self.initialDirection = RIGHT

    def drawBody(self, screen):
        """ Dar snake's Body"""
        for index, i in enumerate(self.snakeBody):
            body = pygame.Rect(i, (GRID_SIZE-3,GRID_SIZE-3))
            if index != len(self.snakeBody)-1:
                pygame.draw.rect(screen, (0,0,0), body)
            else:
                pygame.draw.rect(screen, (255, 0, 0), body)

    def moveBody(self):
        """Move snake's body"""
        self.snakeBody.append(tuple(head+movement for head, movement in zip(self.snakeBody[-1], self.initialDirection)))
        self.snakeBody.pop(0)

    def neuralDirection(self, input):
        """Change direction based on feed forward result
        input is feed forward result array [value1, value2, value3, value4]
        """
        prediction = copy.deepcopy(input)
        direction = np.argmax(prediction)

        if direction == 0 and self.initialDirection != DOWN:
            self.initialDirection = UP
        elif direction == 1  and self.initialDirection != LEFT:
            self.initialDirection = RIGHT
        elif direction == 2  and self.initialDirection != UP:
            self.initialDirection = DOWN
        elif direction == 3  and self.initialDirection != RIGHT:
            self.initialDirection = LEFT