from gamemodel import *
from graphics import *


class GameGraphics:
    def __init__(self, game):
        self.game = game

        self.win = GraphWin("Cannon game", 640, 480, autoflush=False)
        self.win.setCoords(-110, -10, 110, 155)

        self.line = Line(Point(-110, 0), Point(110, 0))
        self.line.setFill('black')
        self.line.draw(self.win)

        self.draw_cannons = [self.drawCanon(0), self.drawCanon(1)]
        self.draw_scores = [self.drawScore(0), self.drawScore(1)]
        self.draw_projs = [None, None]

    def drawCanon(self, playerNr):
        y1 = 0
        y2 = self.game.getCannonSize()
        x1 = self.game.getPlayers()[playerNr].getX() - self.game.getCannonSize()/2
        x2 = self.game.getPlayers()[playerNr].getX() + self.game.getCannonSize()/2
        color = self.game.getPlayers()[playerNr].getColor()

        rect = Rectangle(Point(x1, y1), Point(x2, y2))
        rect.setFill(color)
        rect.draw(self.win)
        return rect

    def drawScore(self, playerNr):

        players = self.game.getPlayers()
        p = players[playerNr].getX()
        score = players[playerNr].getScore()
        score_label = Text(Point(p, -5), 'Score: ' + str(score))
        score_label.draw(self.win)

        return score_label

    def fire(self, angle, vel):
        player = self.game.getCurrentPlayer()
        proj = player.fire(angle, vel)

        circle_X = proj.getX()
        circle_Y = proj.getY()

        playerNr = self.game.getCurrentPlayerNumber()
        if self.draw_projs[playerNr] is not None:
            self.draw_projs[playerNr].undraw()

        circle = Circle(Point(circle_X, circle_Y), self.game.getBallSize())
        circle.draw(self.win)
        circle.setFill(player.getColor())
        self.draw_projs[playerNr] = circle

        while proj.isMoving():
            proj.update(1 / 50)

            circle.move(proj.getX() - circle_X, proj.getY() - circle_Y)

            circle_X = proj.getX()
            circle_Y = proj.getY()

            update(50)

        return proj

    def updateScore(self, playerNr):
        self.draw_scores[playerNr].undraw()
        self.draw_scores[playerNr] = self.drawScore(playerNr)

    def play(self):
        while True:
            player = self.game.getCurrentPlayer()
            oldAngle, oldVel = player.getAim()
            wind = self.game.getCurrentWind()


            inp = InputDialog(oldAngle, oldVel, wind)

            if inp.interact() == "Fire!":
                angle, vel = inp.getValues()
                inp.close()
            elif inp.interact() == "Quit":
                exit()

            player = self.game.getCurrentPlayer()
            other = self.game.getOtherPlayer()
            proj = self.fire(angle, vel)
            distance = other.projectileDistance(proj)

            if distance == 0.0:
                player.increaseScore()
                self.updateScore(self.game.getCurrentPlayerNumber())
                self.game.newRound()

            self.game.nextPlayer()


class InputDialog:
    def __init__(self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0, 4.5, 4, .5)
        Text(Point(1, 1), "Angle").draw(win)
        self.angle = Entry(Point(3, 1), 5).draw(win)
        self.angle.setText(str(angle))

        Text(Point(1, 2), "Velocity").draw(win)
        self.vel = Entry(Point(3, 2), 5).draw(win)
        self.vel.setText(str(vel))

        Text(Point(1, 3), "Wind").draw(win)
        self.height = Text(Point(3, 3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))

        self.fire = Button(win, Point(1, 4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3, 4), 1.25, .5, "Quit")
        self.quit.activate()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a, v

    def close(self):
        self.win.close()


class Button:

    def __init__(self, win, center, width, height, label):
        w, h = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        return self.label.getText()

    def activate(self):
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0


GameGraphics(Game(11, 3)).play()
