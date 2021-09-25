import random
import arcade

class Tree(arcade.Sprite):
    def __init__(self, w, h, s):
        super().__init__()

        self.texture = random.choice([arcade.load_texture('img/tree0.png'),
                                      arcade.load_texture('img/tree1.png')])

        self.center_x = w
        self.center_y = h // 4
        self.speed = s
        self.change_x = -1 * self.speed