"""14.0 BB8 ATTACK GAME   Name: Logan Mills
 
You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 14."""


import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
SW = 800
SH = 600
SP = 4


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.wav")
        self.explosion_sound = arcade.load_sound("sounds/explosion.wav")

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left <= 0:
            self.left = 0
            arcade.play_sound(self.explosion_sound)
            self.change_x = 0
        if self.right >= SW:
            self.right = SW
            arcade.play_sound(self.explosion_sound)
            self.change_x = 0
        if self.bottom <= 0:
            self.bottom = 0
            arcade.play_sound(self.explosion_sound)
            self.change_y = 0
        if self.top >= SH:
            self.top = SH
            arcade.play_sound(self.explosion_sound)
            self.change_y = 0



class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)

    def update(self):
        pass


# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_mouse_visible(False)

    def reset(self):
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()

        # Initiate the score
        self.score = 0

        # Create player
        self.bb8 = Player()
        self.bb8.center_x = SW / 2
        self.bb8.center_y = SH / 2
        self.player_list.append(self.bb8)

        # Create troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w, SW-trooper.w)
            trooper.center_y = random.randrange(trooper.h, SH-trooper.h)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        self.trooper_list.draw()
        self.player_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def on_update(self, dt):
        self.trooper_list.update()
        self.player_list.update()

        trooper_hit_list = arcade.check_for_collision_with_list(self.bb8, self.trooper_list)
        for trooper in trooper_hit_list:
            trooper.kill()
            self.score += 1
            arcade.play_sound(self.bb8.laser_sound)

        if len(self.trooper_list) == 0:
            self.reset()

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.A:
            self.bb8.change_x = -SP
        elif key == arcade.key.D:
            self.bb8.change_x = SP
        elif key == arcade.key.S:
            self.bb8.change_y = -SP
        elif key == arcade.key.W:
            self.bb8.change_y = SP

    def on_key_release(self, key, modifiers: int):
        if key == arcade.key.A or key == arcade.key.D:
            self.bb8.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.bb8.change_y = 0

# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Attack")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
