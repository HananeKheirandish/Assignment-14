import time

import arcade

from ground import Ground
from tree import Tree
from dino import Dino
from bird import Bird

class Game(arcade.Window):
    def __init__(self):
        self.w = 900
        self.h = 500
        super().__init__(self.w, self.h, 'Google Chrome Runner')

        self.background_color = arcade.color.WHITE
        self.background_time = time.time()
        self.morning = 1

        self.gravity = 0.2
        self.start_game = 0
        self.new_game = 0
        self.start_time = time.time()
        
        self.cloud = arcade.Sprite('img/cloud.png')
        self.cloud.width = 200
        self.cloud.height = 100
        self.cloud.center_x = self.w
        self.cloud.center_y = self.h - 100
        self.cloud.change_x = -1

        self.moon = arcade.Sprite('img/moon.png')
        self.moon.width = 40
        self.moon.height = 100
        self.moon.center_x = self.w
        self.moon.center_y = self.h - 200
        self.moon.change_x = -2

        self.me = Dino(self.h)

        self.ground_list = arcade.SpriteList()
        self.ground_list.append(Ground(self.w, self.h))

        self.tree_list = arcade.SpriteList()
        self.tree_time = time.time()
        self.tree_speed = 2

        self.bird_list = arcade.SpriteList()
        self.bird_time = time.time()
        self.bird_speed = 3

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.me, self.ground_list, gravity_constant= self.gravity)
        

    def on_draw(self):
        arcade.start_render()

        if self.me.life == 0:
            arcade.draw_text('GAME OVER', self.w/2-200, self.h/2, arcade.color.RED, 50)
            arcade.draw_text('Press space to start new game', self.w/2-180, self.h/2-50, arcade.color.RED, 20)

        else:
            self.me.draw()

            if self.start_game == 1:
                for ground in self.ground_list:
                    ground.draw()

                for tree in self.tree_list:
                    tree.draw()

                for bird in self.bird_list:
                    bird.draw()

                self.cloud.draw()

                if self.morning == 0:
                    arcade.draw_text(f'Score: {self.me.score}', self.w-150, self.h-50, arcade.color.WHITE, 20)
                    self.moon.draw()
                else:
                    arcade.draw_text(f'Score: {self.me.score}', self.w-150, self.h-50, arcade.color.BLACK, 20)
                
                if self.new_game == 1:
                    if self.morning == 0:
                        arcade.draw_text(f'HI: {self.me.high_score}', self.w-300, self.h-50, arcade.color.WHITE, 20)
                        self.moon.draw()
                    else:
                        arcade.draw_text(f'HI: {self.me.high_score}', self.w-300, self.h-50, arcade.color.BLACK, 20)


    def on_update(self , delta_time):
        self.end_time = time.time()

        if self.start_game == 1:
            if self.end_time - self.background_time > 15 and self.background_color == arcade.color.WHITE:
                self.background_color = arcade.color.BLACK
                self.morning = 0
                self.background_time = time.time()
            elif self.end_time - self.background_time > 10 and self.background_color == arcade.color.BLACK:
                self.background_color = arcade.color.WHITE
                self.morning = 1
                self.background_time = time.time()

            if self.end_time - self.start_time > 0.005:
                self.me.score += 1
                self.start_time = time.time()

            if self.end_time - self.tree_time > 4:
                new_tree = Tree(self.w, self.h, self.tree_speed)
                self.tree_list.append(new_tree)
                self.tree_time = time.time()

            if self.me.score // 100 == 5:
                self.tree_speed += 0.01
                self.bird_speed += 0.02
                self.tree_time = time.time()

            if self.me.score > 1000 and self.end_time - self.bird_time > 10:
                new_bird = Bird(self.w, self.h, self.bird_speed)
                self.bird_list.append(new_bird)
                self.bird_time = time.time()

            for ground in self.ground_list:
                if ground.center_x < -300:
                    self.ground_list.remove(ground)
                    new_ground = Ground(self.w, self.h)
                    self.ground_list.append(new_ground)
            
            for tree in self.tree_list:
                tree.update()
                if tree.center_x < 0 :
                    self.tree_list.remove(tree)

            for bird in self.bird_list:
                bird.update_animation()
                bird.update()
                if bird.center_x < 0:
                    self.bird_list.remove(bird)

            if self.cloud.center_x < 0:
                self.cloud.center_x = self.w
            self.cloud.update()
            
            if self.moon.center_x < 0:
                self.moon.center_x = self.w
            self.moon.update()

            self.physics_engine.update()
            self.me.center_x = 100

            for tree in self.tree_list:
                if arcade.check_for_collision(self.me, tree):
                    self.me.life = 0
                    self.start_game = 0
                    self.tree_list.remove(tree)
                    arcade.play_sound(arcade.sound.Sound(':resources:sounds/gameover2.wav'))

            for bird in self.bird_list:
                if arcade.check_for_collision(self.me, bird):
                    self.me.life = 0
                    self.start_game = 0
                    self.bird_list.remove(bird)
                    arcade.play_sound(arcade.sound.Sound(':resources:sounds/gameover2.wav'))

        self.me.update_animation()

    def start_new_game(self):
        self.start_game = 1
        if self.me.score > self.me.high_score:
            self.me.high_score = self.me.score
        self.me.score = 0
        self.me.life = 1
        self.tree_speed = 2
        self.bird_speed = 3
        self.start_time = time.time()
        self.new_game = 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.start_game = 1
        elif key == arcade.key.DOWN:
            self.me.change_x = 0
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.me.change_y = 11
                arcade.play_sound(arcade.sound.Sound(':resources:sounds/jump1.wav'))
        elif key == arcade.key.SPACE :
            self.start_new_game()

    def on_key_release(self, key, modifiers):
        self.me.change_x = 1
        self.me.change_y = 0

game = Game()
arcade.run()     