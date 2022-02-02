import turtle
import GameLibrary as GLib

"""
John Gutierrez, 5/12/19
Game files from GameLibrary.py
Widow size is 1280x720
global dimensions in GameLibrary

***Notes***:
Ended up pretty good. Some issues with bullets being removed from the list. Probably due to being within the hitbox when
the zombie is destroyed. The level keeps starting at 2 instead of 1. Lag issues with lots of bullets. Zombies and
bullets and player are all solid color shapes. No level titles or anything.
"""

player1 = GLib.Player()
board = GLib.GameBoard(player1)
board.create_borders()
score = GLib.Score()
showLvl = GLib.ShowLevel()
showPHealth = GLib.PlayerHealthDisplay(player1)

zombies = []
bullets = GLib.bullets

while player1.player_health > 0:  # player_health starts at 100

    # check that there are still zombies on screen
    if len(zombies) == 0:
        showLvl.update_level()
        for i in range(1, showLvl.level):
            zombies.append(GLib.Zombie())
            # every fifth level append a boss
            if i % 5 == 0:
                zombies.append(GLib.ZombieBoss())

    # there are still zombies on screen
    else:
        for zombie in zombies:
            # check zombie health first
            if zombie.health <= 0:
                zombie.destroy_zombie()  # remove from screen
                zombies.remove(zombie)  # remove from list
                if type(zombie) is GLib.ZombieBoss:
                    score.update_score(500)
                elif type(zombie) is GLib.Zombie:
                    score.update_score(100)

            # check zombie damaging player
            if zombie.is_player_collision(player1):
                if type(zombie) is GLib.Zombie:
                    player1.change_health(2)  # 2 damage from zombie per hit
                    showPHealth.update_player_health_display(player1)  # show new health
                if type(zombie) is GLib.ZombieBoss:
                    player1.change_health(20)  # 20 damage from zombie bosses
                    showPHealth.update_player_health_display(player1)  # show new health

            # seek after player and move
            zombie.move(player1)

    # Bullet movement and collision
    # no bullets have spawned
    if len(bullets) == 0:
        continue
    # bullets are on screen
    else:
        for bullet in bullets:
            # check if bullet in bounds
            if bullet.is_border_collision():
                bullets.remove(bullet)
                bullet.destroy_bullet()

            # check if bullet has collided with zombie
            for zombie in zombies:
                # bullet hits zombie
                if bullet.is_zombie_collision(zombie):
                    bullets.remove(bullet)
                    bullet.destroy_bullet()
                    zombie.change_health(50)

            # move bullet after checks, bullets move
            bullet.update_bullet()

turtle.exitonclick()
