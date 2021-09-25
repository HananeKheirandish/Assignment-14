import arcade

class Bird(arcade.AnimatedWalkingSprite):
    def __init__(self, w, h, s):
        super().__init__()

        self.walk_left_textures = [arcade.load_texture('img/bird0.png'), arcade.load_texture('img/bird1.png')]

        self.center_x = w
        self.center_y = h // 2 - 10
        self.speed = s 
        self.change_x = -1 * self.speed