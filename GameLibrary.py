import turtle
import math
import random

"""
John Gutierrez, 5/12/19
Game files for Game.py
Includes several classes
"""
# globals
WIDTH = 1280
HEIGHT = 720
bullets = []  # created here so it gets imported by Game


class GameBoard(turtle.Turtle):
    """Creates the game board, sets background.
    Key Binds are set here.
        Functions:
    create_borders - draws border around gameBoard"""

    def __init__(self, player):
        turtle.Turtle.__init__(self)
        self.penup()
        self.hideturtle()
        self.speed(0)

        wn = turtle.Screen()
        wn.setup(WIDTH, HEIGHT, 0, 0)
        wn.bgpic("room.gif")
        wn.listen()
        wn.onkeypress(player.move_forward, "w")
        wn.onkeypress(player.move_left, "a")
        wn.onkeypress(player.move_backward, "s")
        wn.onkeypress(player.move_right, "d")
        wn.onkeypress(player.shoot, "j")

    def create_borders(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.width(10)
        self.hideturtle()
        self.color("gray")
        self.goto(-WIDTH/2, HEIGHT/2)

        self.pendown()
        self.goto(WIDTH/2, HEIGHT/2)
        self.goto(WIDTH/2, -HEIGHT/2)
        self.goto(-WIDTH/2, -HEIGHT/2)
        self.goto(-WIDTH/2, HEIGHT/2)


class Player(turtle.Turtle):
    """
    Creates the player and controls movement, shooting...
        Functions:
    move_left - turns left
    move_right - turns right
    move_forwards - forward
    move_backwards - turns player 180 to face opposite direction
    shoot - spawn bullet at player
    """

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)  # animation speed

        # begin with basic shapes, later change to more detail
        self.shape("triangle")
        self.color("gray")
        self.shapesize(stretch_len=2)

        self.player_speed = 15  # player movement speed
        self.player_health = 1000  # player health

    def move_left(self):
        # turn left
        self.left(15)

    def move_right(self):
        # turn right
        self.right(15)

    def move_forward(self):
        if WIDTH / 2 <= self.xcor() + self.player_speed:
            self.setx(WIDTH/2 - 10)
        if HEIGHT / 2 <= self.ycor() + self.player_speed:
            self.sety(HEIGHT/2 - 10)
        if self.xcor() - self.player_speed <= -WIDTH / 2:
            self.setx(-WIDTH/2 + 10)
        if self.ycor() - self.player_speed <= -HEIGHT / 2:
            self.sety(-HEIGHT/2 + 10)
        # move forward
        else:
            self.forward(self.player_speed)

    def move_backward(self):
        # turn 180 to face other direction
        self.left(180)

    def shoot(self):
        bullets.append(Bullet(self))  # creates a bullet at the player

    def change_health(self, damage):
        self.player_health -= damage


class Zombie(turtle.Turtle):
    """Makes basic zombies that attack the player.
    Zombies have health and movement.
        Functions:
    move - calls seek_player then moves
    seek_player - gets players x and y and moves towards that
    change_health - removes an amount of health from the zombie"""

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.health = 100
        self.speed(0)  # animation speed
        self.zombie_speed = 1.75
        self.shape("circle")
        self.color("white")
        self.goto(random.randint(-WIDTH / 2 + 30, WIDTH / 2 - 30), random.randint(-HEIGHT / 2 + 30, HEIGHT / 2 - 30))

    def move(self, player):
        self.seek_player(player)  # sets heading
        self.forward(self.zombie_speed)  # move in that direction

    def seek_player(self, player):
        x, y = player.xcor(), player.ycor()
        delta_x = x - self.xcor()
        delta_y = y - self.ycor()

        # blatant absolute value of angle
        angle = math.degrees(abs(math.atan(abs(delta_y) / abs(delta_x))))

        # Quad 1
        if (delta_x > 0) and (delta_y > 0):
            self.setheading(angle)
        # QUAD 2
        if (delta_x < 0) and (delta_y > 0):
            self.setheading(180 - angle)
        # QUAD 3
        if (delta_x < 0) and (delta_y < 0):
            self.setheading(180 + angle)
        # QUAD 4
        if (delta_x > 0) and (delta_y < 0):
            self.setheading(360 - angle)
        # errors when both objects on same x or y plane
        if delta_x == 0:
            if delta_y < 0:
                self.setheading(270)
            else:
                self.setheading(90)
        if delta_y == 0:
            if delta_x < 0:
                self.setheading(180)
            else:
                self.setheading(0)

    def change_health(self, damage):
        self.health -= damage

    def is_player_collision(self, player):
        if (player.xcor() - 10) <= self.xcor() <= (player.xcor() + 10) \
                and (player.ycor() - 10) <= self.ycor() <= (player.ycor() + 10):
            return True
        else:
            return False

    def destroy_zombie(self):
        self.clear()
        self.hideturtle()


class ZombieBoss(Zombie):
    """Inherits attributes from zombie.
    A bigger zombie with more health.
        Functions:
    Same as regular zombie, just bigger initializing."""

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        self.goto(random.randint(-WIDTH / 2 + 30, WIDTH / 2 - 30), random.randint(-HEIGHT / 2 + 30, HEIGHT / 2 - 30))
        self.shape("circle")
        self.color("white")
        self.shapesize(stretch_wid=5)
        self.health = 300
        self.zombie_speed = 0.5


class Score(turtle.Turtle):
    """will create a text at the bottom left that displays score.
        Functions:
    update_score - displays the new score with points added"""

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        # bottom left but over a bit to show text
        self.goto(-WIDTH/2 + 30, -HEIGHT/2 + 30)
        self.hideturtle()
        self.speed(0)
        self.color("White")
        self.score = 0
        # initializes the text
        self.write(f"Score: {self.score}", move=False, align="left", font=("Arial", 16, "normal"))

    def update_score(self, points):
        self.clear()
        self.score += points
        self.write(f"Score: {self.score}", move=False, align="left", font=("Arial", 16, "normal"))


class Bullet(turtle.Turtle):
    """
    Will control bullet movement and destruction.
        Functions:
    update_bullet - will check for collisions and movement
    destroy_bullet - erases bullet
    is_zombie_collision - detects collision with a given zombie
    is_border_collision - determines whether bullet has left the game
    """

    def __init__(self, player):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.goto(player.xcor(), player.ycor())  # bullet spawns at player's position
        self.setheading(player.heading())  # bullet will go in direction of player
        self.shape("circle")
        self.color("white")
        self.shapesize(stretch_len=1)
        self.bulletSpeed = 15  # bullet speed
        self.bulletDamage = 5  # bullet damage

    def is_zombie_collision(self, zombie):
        # collision with given zombie
        # hitbox is 10x10
        if (zombie.xcor() - 10 <= self.xcor() <= zombie.xcor() + 10) and (zombie.ycor() - 10 <= self.ycor() <= zombie.ycor()) + 10:
            zombie.change_health(self.bulletDamage)
            return True
        else:
            return False

    def is_border_collision(self):
        # collision with border
        # hitbox is 10x10
        if (WIDTH/2 <= self.xcor()) or (self.xcor() <= -WIDTH/2) or (HEIGHT/2 <= self.ycor()) or (self.ycor() <= -HEIGHT/2):
            return True
        else:
            return False

    def update_bullet(self):
        self.forward(self.bulletSpeed)

    def destroy_bullet(self):
        self.clear()
        self.hideturtle()


class ShowLevel(turtle.Turtle):
    """will create a text at the bottom right that displays level.
            Functions:
        update_level - displays the next level"""

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        # bottom left but over a bit to show text
        self.goto(WIDTH / 2 - 100, -HEIGHT / 2 + 30)  # level is bottom right
        self.hideturtle()
        self.speed(0)
        self.color("White")
        self.level = 0
        # initializes the text
        self.write(f"Level: {self.level}", move=False, align="left", font=("Arial", 16, "normal"))

    def update_level(self):
        self.clear()
        self.level += 1
        self.write(f"Level: {self.level}", move=False, align="left", font=("Arial", 16, "normal"))


class PlayerHealthDisplay(turtle.Turtle):
    """
    will show a bar or text of the player's health above the player
    """
    def __init__(self, player):
        turtle.Turtle.__init__(self)
        self.penup()
        self.hideturtle()
        self.goto(-WIDTH/2 + 30, -HEIGHT/2 + 30 + 30)  # health will be above score
        self.speed(0)
        self.color("white")

        self.write(f"Health: {player.player_health}", move=False, align="left", font=("Ariel", 16, "normal"))

    def update_player_health_display(self, player):
        self.clear()
        self.write(f"Health: {player.player_health}", move=False, align="left", font=("Ariel", 16, "normal"))

