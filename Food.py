"""
This py controll food visualization and position
"""
from Parameters import *

class Food():
    def __init__(self):
        """
        Foodsize is rectangle with size GridSizexGridSize
        initially give position and after that randomly draw food position
        """

        self.foodSize = (GRID_SIZE,GRID_SIZE)
        self.foodPosition = (0,SCREEN_HEIGHT-GRID_SIZE)
        self.grow = 0

    def foodCollision(self, snake):
        """
        Controlling event when snake collides with food, when scores get 30 i amslowing down grow rate for training purpose
        :return: True if snake colides food, False if Snake not colide food
        """
        collision = False
        if snake.snakeBody[-1] == self.foodPosition:
           collision = True
           while self.foodPosition in snake.snakeBody:
               self.foodPosition = (random.randint(0, (SCREEN_WIDTH/GRID_SIZE)-2) * GRID_SIZE, random.randint(0, (SCREEN_HEIGHT/GRID_SIZE)-2) * GRID_SIZE)
           if len(snake.snakeBody) < 30:
               snake.snakeBody.append(snake.snakeBody[-1])
           elif len(snake.snakeBody) >= 30 and self.grow != 2:
               snake.snakeBody.append(snake.snakeBody[-1])
               self.grow +=1
           if self.grow == 2:
               self.grow = 0
        return collision, snake.snakeBody

    def draw(self, screen):
        food = pygame.image.load("Pictures/Tomatos.png")
        screen.blit(food, self.foodPosition)