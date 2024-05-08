"""
FINAL GAME PROJECT
------------------
Here you will start the beginning of a game that you will be able to update as we
learn more in upcoming chapters. Below are some ideas that you could include:

1.) Find some new sprite images.
2.) Move the player sprite with arrow keys rather than the mouse. Don't let it move off the screen.
3.) Move the other sprites in some way like moving down the screen and then re-spawning above the window.
4.) Use sounds when a sprite is killed or the player hits the sidewall.
5.) See if you can reset the game after 30 seconds. Remember the on_update() method runs every 1/60th of a second.
6.) Try some other creative ideas to make your game awesome. Perhaps collecting good sprites while avoiding bad sprites.
7.) Keep score and use multiple levels. How do you keep track of an all-time high score?
8.) Make a two player game.

"""

import random
import arcade

# --- Constants ---
sw = 960
sh = 600
fruitCount = 16


class Fruit(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/Fruits/fruit0000.png")
        self.textures = texture_list
        self.current_texture = random.randint(0, 15)
        self.set_texture(self.current_texture)
        self.dx = 0
        self.dy = random.randint(12, 15)
        self.da = random.randrange(-5, 5, 2)

    def update(self):
        self.dy -= 0.18

        self.angle += self.da
        self.center_x += self.dx
        self.center_y += self.dy

        if self.top < 0:
            self.kill()

class Bomb(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bomb.png", 0.2)
        self.dx = 0
        self.dy = random.randint(12, 15)
        self.da = random.randrange(-5, 5, 2)

    def update(self):
        self.dy -= 0.18

        self.angle += self.da
        self.center_x += self.dx
        self.center_y += self.dy

        if self.top < 0:
            self.kill()


# ------MyGame Class--------------
# noinspection PyAttributeOutsideInit


class MyGame(arcade.Window):
    def __init__(self, sw, sh, title):
        super().__init__(sw, sh, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.fruit_texture_list = []
        self.time = 0

        self.background = arcade.load_texture("Images/background.jpeg")

        # Load all fruits
        for i in range(fruitCount):
            texture_name = f"Images/Fruits/fruit{i:04}.png"
            self.fruit_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):
        # Make sprite lists
        self.fruit_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Reset Score related things
        self.gameOver = False
        self.score = 0
        self.strikes = 0


    def on_draw(self):
        # Gameplay
        if not self.gameOver:
            arcade.draw_texture_rectangle(sw/2, sh/2, sw, sh, self.background)
            self.fruit_list.draw()
            self.bomb_list.draw()
            self.player_list.draw()
        # Gameover Screen
        else:
            pass

    def on_update(self, dt):
        if not self.gameOver:
            self.fruit_list.update()
            self.bomb_list.update()
            self.player_list.update()



            self.time += dt  # Add to timer
            # jitter = random.randint(50, 90)  # Randomized timing

            if self.time >= 1.5:  # When it hits that time
                if random.randint(0, 3) == 0:  # Random number for bomb or fruit
                    bomb = Bomb()
                    bomb.center_x = random.randint(0, sw)
                    if bomb.center_x >= sw / 2:
                        bomb.dx = random.randrange(-3, -1)
                    else:
                        bomb.dx = random.randrange(1, 3)
                    bomb.top = 0
                    self.bomb_list.append(bomb)
                    self.time = 0
                else:
                    fruit = Fruit(self.fruit_texture_list)
                    fruit.center_x = random.randint(0, sw)
                    if fruit.center_x >= sw / 2:
                        fruit.dx = random.randrange(-3, -1)
                    else:
                        fruit.dx = random.randrange(1, 3)
                    fruit.top = 0
                    self.fruit_list.append(fruit)
                    self.time = 0



# -----Main Function--------
def main():
    window = MyGame(sw, sh, "My Game")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
