"""This pt setting up snake's visions in 8 directions"""
from Parameters import *

class Vector():
    def __init__(self, snake, food):
        """

        :param snake: set up for snake class
        :param food: set up for food class
        vector is a set of vector from snake head to wall in 8 directions
        """
        self.snake = snake
        self.food = food
        self.vector = self.calculateVector()

    def checkWall(self):
        """Check distance from head to end of vector or vector[-1] (because self.vector is from head to wall
        North, East, South, West, NorthEast, SouthEast, SouthSouthWest, NorthWest index is 0,1,2,3,4,5,6,7

        Distance is 1/d
        """
        coordinate = self.vector

        northWallDistance = calculateDistanceTwoCoordinate(coordinate[0][0], coordinate[0][-1])
        if northWallDistance <= 0:
            northWallDistance = 1
        else:
            northWallDistance = 1/northWallDistance

        eastWallDistance = calculateDistanceTwoCoordinate(coordinate[1][0], coordinate[1][-1])
        if eastWallDistance <= 0:
            eastWallDistance = 1
        else:
            eastWallDistance = 1/eastWallDistance

        southWallDistance = calculateDistanceTwoCoordinate(coordinate[2][0], coordinate[2][-1])
        if southWallDistance <= 0:
            southWallDistance = 1
        else:
            southWallDistance = 1/southWallDistance

        westWallDistance = calculateDistanceTwoCoordinate(coordinate[3][0], coordinate[3][-1])
        if westWallDistance <= 0:
            westWallDistance = 1
        else:
           westWallDistance = 1/westWallDistance

        northEastWallDistance = calculateDistanceTwoCoordinate(coordinate[4][0], coordinate[4][-1])
        if northEastWallDistance <= 0:
            northEastWallDistance = 1
        else:
            northEastWallDistance = 1/northEastWallDistance

        southEastWallDistance = calculateDistanceTwoCoordinate(coordinate[5][0], coordinate[5][-1])
        if southEastWallDistance <= 0:
            southEastWallDistance = 1
        else:
            southEastWallDistance = 1/southEastWallDistance

        southWestWallDistance = calculateDistanceTwoCoordinate(coordinate[6][0], coordinate[6][-1])
        if southWestWallDistance <= 0:
            southWestWallDistance = 1
        else:
            southWestWallDistance = 1/southWestWallDistance

        northWestWallDistance = calculateDistanceTwoCoordinate(coordinate[7][0], coordinate[7][-1])
        if northWestWallDistance <= 0:
            northWestWallDistance = 1
        else:
            northWestWallDistance = 1/northWestWallDistance

        return [northWallDistance,eastWallDistance,southWallDistance,westWallDistance,northEastWallDistance,southEastWallDistance,southWestWallDistance,northWestWallDistance]

    def checkFood(self):
        """Check" wheter within vector lies food position
        if there is a food then distance is 1, else = 0"""
        coordinate = self.vector

        distanceFood = []
        real = []

        for index, position in enumerate(coordinate):
            if self.food.foodPosition in position:

                distanceFood.append(1)
                d = calculateDistanceTwoCoordinate(self.food.foodPosition, position[0])
                if d==0:
                    real.append(1)
                else:
                    real.append(1/d)
            else:
                real.append(0)
                distanceFood.append(0)

        return distanceFood, real


    def checkBody(self):
        """Checking wether within vector there is snake body or no
        distance is 1/d
        snake body lies in opposite snake direction counted from 2nd body from head (if any)
        """
        coordinate = self.vector

        distance = [0,0,0,0,0,0,0,0]
        head = self.snake.snakeBody[-1]
        for index, coordinateset in enumerate(coordinate):
            for number, coor in enumerate(coordinateset):
                if coor in self.snake.snakeBody[:-2]:

                    d = calculateDistanceTwoCoordinate(head, coor)
                    if d==0:
                        distance[index] = 1
                    else:
                        distance[index] = 1/d
                    break
        return distance


    def checkObject(self):
        """Compile all distance into 1 vector
        if there is body distance then food distance and wall distance will be set to 0 if
        snake bidy have higher distance than food (since disntace is 1/d)"""
        wallDistance = self.checkWall()
        foodDistance, real = self.checkFood()
        bodyDistance = self.checkBody()

        if self.snake.initialDirection == RIGHT:
            wallDistance[3] = 0
            foodDistance[3] = 0
            bodyDistance[3] = 0
        elif self.snake.initialDirection == DOWN:
            wallDistance[0] = 0
            foodDistance[0] = 0
            bodyDistance[0] = 0
        elif self.snake.initialDirection == LEFT:
            wallDistance[1] = 0
            foodDistance[1] = 0
            bodyDistance[1] = 0
        elif self.snake.initialDirection == UP:
            wallDistance[2] = 0
            foodDistance[2] = 0
            bodyDistance[2] = 0

        for index, DistanceSet in enumerate(bodyDistance):
            if DistanceSet !=0 and DistanceSet>real[index]:
                foodDistance[index] = 0
            elif DistanceSet != 0 and DistanceSet>wallDistance[index]:
                wallDistance[index] = 0
        return wallDistance,foodDistance, bodyDistance

    def calculateVector(self):
        """Calculate every vector in 8 direction from head to wall"""
        head = self.snake.snakeBody[-1]

        northVector = self.createSetOfVector(head, "North")
        eastVector =  self.createSetOfVector(head, "East")
        southVector =  self.createSetOfVector(head, "South")
        westVector = self.createSetOfVector(head, "West")
        northEastVector = self.createSetOfVector(head, "NorthEast")
        southEastVector = self.createSetOfVector(head, "SouthEast")
        southWestVector = self.createSetOfVector(head, "SouthWest")
        northWestVector = self.createSetOfVector(head, "NorthWest")

        allVector = [northVector, eastVector, southVector, westVector, northEastVector, southEastVector, southWestVector, northWestVector]

        return allVector


    def createSetOfVector(self, head, position):
        """
        Calculate every coordiante in each direction from head until reach wall
        :param head:
        :param position:
        :return: set of direction
        """
        currentX = head[0]
        currentY = head[1]

        if position == "North" or position == "West":
            if position == "North":
                vector = np.arange(0, currentY + GRID_SIZE, GRID_SIZE)
                coordinate = [(currentX, j) for j in vector]
                coordinate = coordinate[::-1]

            elif position == "West":
                vector = np.arange(0, currentX + GRID_SIZE, GRID_SIZE)
                coordinate = [(i, currentY) for i in vector]
                coordinate = coordinate[::-1]

        elif position == "East" or position == "South":
            if position == "East":
                vector = np.arange(currentX, SCREEN_WIDTH, GRID_SIZE)
                coordinate = [(i, currentY) for i in vector]


            elif position == "South":
                vector = np.arange(currentY, SCREEN_HEIGHT, GRID_SIZE)
                coordinate = [(currentX, j) for j in vector]

        elif position == "NorthEast":
            x = currentX
            y = currentY
            coordinate = []

            while True:
                coordinate.append((x, y))

                x += GRID_SIZE
                y -= GRID_SIZE

                if x > SCREEN_WIDTH-GRID_SIZE or y < 0:
                    break

        elif position == "SouthEast":
            x = currentX
            y = currentY
            coordinate = []
            while True:
                coordinate.append((x, y))
                x += GRID_SIZE
                y += GRID_SIZE

                if x > SCREEN_WIDTH-GRID_SIZE or y > SCREEN_HEIGHT-GRID_SIZE:
                    break

        elif position == "SouthWest":
            x = currentX
            y = currentY
            coordinate = []
            while True:
                coordinate.append((x, y))
                x -= GRID_SIZE
                y += GRID_SIZE

                if x < 0 or y > SCREEN_HEIGHT-GRID_SIZE:
                    break

        elif position == "NorthWest":
            x = currentX
            y = currentY
            coordinate = []
            while True:
                coordinate.append((x, y))
                x -= GRID_SIZE
                y -= GRID_SIZE

                if x < 0 or y < 0:
                    break
        return coordinate

@jit(nopython=True)
def calculateDistanceTwoCoordinate(start, end):
    vector = [i-j for i,j in zip(start,end)]
    distance = np.sqrt(vector[0] ** 2 + vector[1] ** 2)
    return distance
