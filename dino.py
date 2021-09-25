import arcade

class Dino(arcade.AnimatedWalkingSprite):
    def __init__(self, h):
        super().__init__()

        self.stand_right_textures = [arcade.load_texture('img/dino-idle.png')]

        self.walk_right_textures = [arcade.load_texture('img/dino-walk0.png'),
                                    arcade.load_texture('img/dino-walk1.png')]

        self.walk_down_textures = [arcade.load_texture('img/stoop0.png'),
                                    arcade.load_texture('img/stoop1.png')]

        self.width = 80
        self.height = 100
        self.center_x = 80
        self.center_y = h // 2 
        self.life = 1
        self.score = 0
        self.high_score = 0