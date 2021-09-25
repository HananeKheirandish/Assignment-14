import arcade

class Ground(arcade.Sprite):
    def __init__(self, w, h):
        super().__init__()

        self.texture = arcade.load_texture('img/ground.png')

        self.h = 20
        self.center_x = w
        self.center_y = h // 5 
        self.speed = 2
        self.change_x = -1 * self.speed