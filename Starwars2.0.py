"""14.0 BB8 ATTACK GAME   Name: Logan Mills

You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 14."""

import random
import arcade
import math

# --- Constants ---
BB8_scale = 0.17
trooper_scale = 0.085
bullet_scale = 0.8
SW = 800
SH = 600
SP = 4
ASP = 5
MSP = 5
bullet_speed = 10
trooper_speed = 2
# points for shooting bullets and troopers
t_score = 5
b_score = 1

'''
0 = Instructions
1-3 = Gameplay
4+ = Game Over
'''
trooper_count = [0, 2, 4, 8]
levels = len(trooper_count)

EXPLOSION_TEXTURE_COUNT = 50


class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/explosions/explosion0000.png")
        self.textures = texture_list
        self.current_texture = 0

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/millenium-falcon.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.wav")
        self.explosion = arcade.load_sound("sounds/explosion.wav")
        self.speed = 0
        self.change_angle = 0

    def update(self):
        self.angle += self.change_angle
        angle_rad = math.radians(self.angle)

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        if self.left < 0:
            self.left = 0
        elif self.right > SW:
            self.right = SW
        elif self.top > SH:
            self.top = SH
        elif self.bottom < 0:
            self.bottom = 0


class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/tie fighter.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)
        self.dx = random.randrange(-1, 2, 2)
        self.dy = random.randrange(-1, 2, 2)

    def update(self):
        self.center_y += self.dy
        self.center_x += self.dx

        if self.top > SH or self.bottom < 0:
            self.dy *= -1
        if self.right > SW or self.left < 0:
            self.dx *= -1


class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.explosion_sound = arcade.load_sound("sounds/explosion.wav")
        self.speed = 0

    def update(self):
        angle_shoot = math.radians(self.angle - 90)

        self.center_x += -self.speed * math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)

        if self.bottom > SH or self.top < 0 or self.left > SW or self.right < 0:
            self.kill()


class EnemyBullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.angle_list = [0, 90, 180, 270]
        self.angle = random.choice(self.angle_list)

    def update(self):
        if self.angle == 0:
            self.center_x += bullet_speed
        elif self.angle == 90:
            self.center_y += bullet_speed
        elif self.angle == 180:
            self.center_x -= bullet_speed
        elif self.angle == 270:
            self.center_y -= bullet_speed

        if self.bottom > SH or self.top < 0 or self.left > SW or self.right < 0:
            self.kill()


# ------MyGame Class--------------
# noinspection PyAttributeOutsideInit
class MyGame(arcade.Window):

    def __init__(self, sw, sh, title):
        super().__init__(sw, sh, title)
        arcade.set_background_color(arcade.color.BLACK)
        # Initiate the score
        self.current_level = 0
        self.score = 0
        self.gameOver = False
        self.set_mouse_visible(False)
        self.highScore = 0
        self.name = ""

        # Preload the explosion textures
        self.explosion_texture_list = []
        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ebullet_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()

        if self.current_level in range(1, levels+1):
            if self.current_level <= 3:
                self.background = arcade.load_texture(f"Images/sky{self.current_level}.png")

            # Create player
            self.bb8 = Player()
            self.bb8.center_x = SW / 2
            self.bb8.center_y = SH / 2
            self.player_list.append(self.bb8)

            # Create troopers
            for i in range(trooper_count[self.current_level]):
                trooper = Trooper()
                if i % 2 == 0:
                    trooper.center_x = random.randrange(trooper.w, int(SW / 3))
                    trooper.center_y = random.randrange(trooper.h, SH-trooper.h)
                else:
                    trooper.center_x = random.randrange(int(SW * 2 / 3), SW - trooper.w)
                    trooper.center_y = random.randrange(trooper.h, SH - trooper.h)

                self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        if self.current_level == 0:
            arcade.draw_rectangle_filled(SW/2, SH/2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use A and D to move BB8 left and right and Space to shoot. Press R to play", SW/2, SH/2 + 30, arcade.color.YELLOW, 14, 400, anchor_x="center")

        elif not self.gameOver:
            arcade.draw_texture_rectangle(SW/2, SH/2, SW, SH, self.background)
            self.trooper_list.draw()
            self.player_list.draw()
            self.bullet_list.draw()
            self.ebullet_list.draw()
            self.explosion_list.draw()

            output = f"Score: {self.score}"
            arcade.draw_text(output, SW-220, SH-20, arcade.color.YELLOW, 14, 200, "right")
            output2 = f"High Score: {self.highScore}"
            arcade.draw_text(output2, SW - 220, SH - 40, arcade.color.YELLOW, 14, 200, "right")
            output3 = f"Level: {self.current_level}"
            arcade.draw_text(output3, SW - 220, SH - 60, arcade.color.YELLOW, 14, 200, "right")
            output4 = f"Troopers: {len(self.trooper_list)}"
            arcade.draw_text(output4, SW - 220, SH - 80, arcade.color.YELLOW, 14, 200, "right")

        # Draw Game over Screen
        else:
            arcade.draw_rectangle_filled(SW/2, SH/2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game Over", SW / 2, SH / 2 + 80, arcade.color.YELLOW, 40, anchor_x="center", anchor_y="center")
            arcade.draw_text(f"Your Score: {self.score}", SW/2, SH/2 + 30, arcade.color.YELLOW, 14, anchor_x="center", anchor_y="center")
            arcade.draw_text("Press [R] to restart!", SW/2, 40, arcade.color.YELLOW, 14, anchor_x="center", anchor_y="center")

    def on_update(self, dt):
        if self.current_level in range(1, levels+1):
            self.gameOver = False

        else:
            self.gameOver = True

        if not self.gameOver:
            self.trooper_list.update()
            self.player_list.update()
            self.bullet_list.update()
            self.ebullet_list.update()
            self.explosion_list.update()

            if self.score > self.highScore:  # Update highscore
                self.highScore = self.score

            if len(self.trooper_list) == 0:  # Game over if all troopers gone
                self.current_level += 1
                self.reset()

            bb8_hit = arcade.check_for_collision_with_list(self.bb8, self.trooper_list)  # Check for collision with trooper
            if len(bb8_hit) > 0 and not self.gameOver:
                self.bb8.kill()  # Kill BB8 if collision detected
                arcade.play_sound(self.bb8.explosion)
                self.current_level = levels + 1

            for bullet in self.bullet_list:  # Collision with bullet and trooper
                hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
                if len(hit_list) > 0:
                    arcade.play_sound(self.bb8.explosion)
                    bullet.kill()  # Kill bullet
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = hit_list[0].center_x
                    explosion.center_y = hit_list[0].center_y
                    self.explosion_list.append(explosion)
                for trooper in hit_list:
                    trooper.kill()  # Kill trooper
                    self.score += t_score

            # Randomly drop nukes

            for trooper in self.trooper_list:
                if random.randrange(1000) == 1:
                    ebullet = EnemyBullet()
                    ebullet.center_x = trooper.center_x
                    ebullet.center_y = trooper.center_y
                    self.ebullet_list.append(ebullet)

            # Kill BB8 if he gets nuked

            BB8_Bombed = arcade.check_for_collision_with_list(self.bb8, self.ebullet_list)
            if len(BB8_Bombed) > 0 and not self.gameOver:
                self.current_level = levels + 1

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.A:
            self.bb8.change_angle = ASP
        elif key == arcade.key.D:
            self.bb8.change_angle = -ASP
        if key == arcade.key.W:
            self.bb8.speed = MSP
        elif key == arcade.key.S:
            self.bb8.speed = -MSP

        if key == arcade.key.SPACE and not self.gameOver:
            bullet = Bullet()
            bullet.center_x = self.bb8.center_x
            bullet.center_y = self.bb8.center_y
            bullet.angle = self.bb8.angle + 90
            bullet.speed = bullet_speed
            self.score -= b_score
            arcade.play_sound(self.bb8.laser_sound)
            self.bullet_list.append(bullet)

        if key == arcade.key.R and self.gameOver:
            self.current_level = 1
            self.score = 0
            self.reset()
        elif key == arcade.key.I and self.gameOver:
            self.current_level = 0

    def on_key_release(self, key, modifiers: int):
        if key == arcade.key.A or key == arcade.key.D:
            self.bb8.change_angle = 0
        if key == arcade.key.W or key == arcade.key.S:
            self.bb8.speed = 0

# -----Main Function--------


def main():
    window = MyGame(SW, SH, "BB8 Attack")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()
