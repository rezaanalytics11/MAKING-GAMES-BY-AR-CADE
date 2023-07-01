import arcade
import random
import os


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Sprite with Moving Platforms'
SPRITE_SCALING = 0.5


SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * SPRITE_SCALING)

VIEWPORT_MARGIN = SPRITE_PIXEL_SIZE * SPRITE_SCALING
RIGHT_MARGIN = 4 * SPRITE_PIXEL_SIZE * SPRITE_SCALING

MOVEMENT_SPEED = 10 * SPRITE_SCALING
JUMP_SPEED = 28 * SPRITE_SCALING
GRAVITY = .9 * SPRITE_SCALING


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Menu Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.all_wall_list = None
        self.static_wall_list = None
        self.moving_wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.end_of_map = 0
        self.time_taken = 0

        self.player_list = arcade.SpriteList()
        self.all_wall_list= arcade.SpriteList()
        self.static_wall_list= arcade.SpriteList()
        self.moving_wall_list = arcade.SpriteList()




        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 3 * GRID_PIXEL_SIZE
        self.score = 0


        for i in range(30):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
            wall.bottom = 0
            wall.center_x = i * GRID_PIXEL_SIZE
            self.static_wall_list.append(wall)
            self.all_wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = random.randint(1,7) * GRID_PIXEL_SIZE
        wall.center_x = 150
        wall.change_y = -random.randint(2, 8) * SPRITE_SCALING
        wall.boundary_top = random.randint(5, 7) * GRID_PIXEL_SIZE
        wall.boundary_bottom = 1 * GRID_PIXEL_SIZE
        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = random.randint(1,7) * GRID_PIXEL_SIZE
        wall.center_x = 300
        wall.change_y = -random.randint(2,8) * SPRITE_SCALING
        wall.boundary_top = random.randint(5,7) * GRID_PIXEL_SIZE
        wall.boundary_bottom = 1 * GRID_PIXEL_SIZE
        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = random.randint(1,7) * GRID_PIXEL_SIZE
        wall.center_x = 450
        wall.change_y = -random.randint(2,8) * SPRITE_SCALING
        wall.boundary_top = random.randint(5,7) * GRID_PIXEL_SIZE
        wall.boundary_bottom = 1 * GRID_PIXEL_SIZE
        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)
        wall.center_y = random.randint(1,7) * GRID_PIXEL_SIZE
        wall.center_x = 600
        wall.change_y = -random.randint(2,8) * SPRITE_SCALING
        wall.boundary_top = random.randint(5,7) * GRID_PIXEL_SIZE
        wall.boundary_bottom = 1 * GRID_PIXEL_SIZE
        self.all_wall_list.append(wall)
        self.moving_wall_list.append(wall)

        self.physics_engine = \
            arcade.PhysicsEnginePlatformer(self.player_sprite,
                                           self.all_wall_list,
                                           gravity_constant=GRAVITY)


    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.player_list.draw()
        self.static_wall_list.draw()
        self.moving_wall_list.draw()

        output = f"Score: {self.score}"
        #arcade.draw_text(output, 10, 30, arcade.color.WHITE, 14)
        output_total = f"Total Score: {self.window.total_score}"
        #arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

        distance = self.player_sprite.right
        output = f"Distance: {distance}"
        arcade.draw_text(output, self.view_left + 10, self.view_bottom + 20,
        arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


    def on_update(self, delta_time):
        self.time_taken += delta_time
        self.physics_engine.update()

        for self.wall in self.all_wall_list:

         hit_list = arcade.check_for_collision_with_list(self.wall, self.player_list)

         for self.wall in hit_list:
            self.wall.kill()
            self.score =0
            self.window.total_score = 0


         if len(self.player_list) == 0:
                game_over_view = GameOverView()
                game_over_view.time_taken = self.time_taken
                self.window.set_mouse_visible(True)
                self.window.show_view(game_over_view)


         if (self.player_sprite.right < -39) and (self.player_sprite.top < -20):
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)


         if (len(self.player_list) !=0) and (self.player_sprite.right>700):
                self.score = 1
                self.window.total_score = 1
                game_over_view = GameWinView()
                game_over_view.time_taken = self.time_taken
                self.window.set_mouse_visible(True)
                self.window.show_view(game_over_view)

        changed = False

        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)



class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         SCREEN_WIDTH / 2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)



class GameWinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Congradulations, You Won !!", 240, 400, arcade.color.WHITE, 40)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}",
                         SCREEN_WIDTH / 2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, SCREEN_WIDTH//3, 100, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()