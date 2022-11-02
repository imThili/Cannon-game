from math import sin, cos, radians
import random


class Game:

    def __init__(self, cannonSize, ballSize):
        self.players = [Player(self, False, -90, "blue"), Player(self, True, 90, "red")]
        self.currentPlayerNumber = 0
        self.currentWind = random.uniform(-10.00, 10.00)
        self.cannonSize = cannonSize
        self.ballSize = ballSize

    def getPlayers(self):
        return self.players

    def getCannonSize(self):
        return self.cannonSize

    def getBallSize(self):
        return self.ballSize

    def getCurrentPlayer(self):
        return self.players[self.currentPlayerNumber]

    def getOtherPlayer(self):
        if self.currentPlayerNumber == 0:
            return self.players[1]
        return self.players[0]

    def getCurrentPlayerNumber(self):
        return self.currentPlayerNumber

    def nextPlayer(self):
        if self.currentPlayerNumber == 0:
            self.currentPlayerNumber = 1
        else:
            self.currentPlayerNumber = 0
        return self.players[self.currentPlayerNumber]

    def setCurrentWind(self, wind):
        self.currentWind = wind

    def getCurrentWind(self):
        return self.currentWind

    def newRound(self):
        self.currentWind = random.uniform(-10.00, 10.00)


class Player:
    def __init__(self, game, isReversed, shooting_direction, color):
        self.game = game
        self.isReversed = isReversed
        self.shooting_direction = shooting_direction
        self.color = color
        self.angle = 45
        self.velocity = 40
        self.score = 0

    def fire(self, angle, velocity):
        self.angle = angle
        self.velocity = velocity
        if self.isReversed:
            newAngle = 180 - angle
        else:
            newAngle = angle
        return Projectile(newAngle, velocity, self.game.getCurrentWind(),
                          self.shooting_direction, self.game.getCannonSize() / 2, -110, 110)

    def projectileDistance(self, proj):
        xValueLeftCannonSide = self.shooting_direction - self.game.getCannonSize() / 2
        xValueRightCannonSide = self.shooting_direction + self.game.getCannonSize() / 2
        xValueLeftBallSide = proj.getX() - self.game.getBallSize()
        xValueRightBallSide = proj.getX() + self.game.getBallSize()

        if self.isReversed:
            if xValueLeftCannonSide <= xValueRightBallSide and xValueLeftBallSide <= xValueRightCannonSide:
                return 0

            elif xValueLeftBallSide > xValueRightCannonSide:
                return xValueLeftBallSide - xValueRightCannonSide

            else:
                return xValueRightBallSide - xValueLeftCannonSide

        else:
            if xValueLeftCannonSide <= xValueRightBallSide and xValueLeftBallSide <= xValueRightCannonSide:
                return 0

            elif xValueRightBallSide < xValueLeftCannonSide:
                return xValueRightBallSide - xValueLeftCannonSide

            else:
                return xValueLeftBallSide - xValueRightCannonSide

    def getScore(self):
        return self.score

    def increaseScore(self):
        newScore = self.score + 1
        self.score = newScore

    def getColor(self):
        return self.color

    def getX(self):
        return self.shooting_direction

    def getAim(self):
        return self.angle, self.velocity


class Projectile:

    def __init__(self, angle, velocity, wind, xPos, yPos, xLower, xUpper):
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity * cos(theta)
        self.yvel = velocity * sin(theta)
        self.wind = wind

    def update(self, time):
        yvel1 = self.yvel - 9.8 * time
        xvel1 = self.xvel + self.wind * time

        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0

        self.yPos = max(self.yPos, 0)

        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)

        self.yvel = yvel1
        self.xvel = xvel1

    def isMoving(self):
        return 0 < self.getY() and self.xLower < self.getX() < self.xUpper

    def getX(self):
        return self.xPos

    def getY(self):
        return self.yPos
