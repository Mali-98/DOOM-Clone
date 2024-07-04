from sprite_object import *


paths = ['resources/sprites/weapon/Nukem_Shotgun/0.png', 'resources/sprites/weapon/Nukem_Super_shotgun/0.png', 'resources/sprites/weapon/Nukem_Golden_Gun/0.png']
weapon_index = 0
scaling = 0.6
animation_duration = 90
hit_damage = 100
rocket_launcher_ammo = 5
golden_gun_ammo = 25
shotgun_ammo = 20
super_shotgun_ammo = 6
#shotgun_recovery_delay=2000
#super_shotgun_recovery_delay=3000
#rocket_launcher_recovery_delay=5000
class Weapon(AnimatedSprite):
    def __init__(self, game):
        self.path = paths[weapon_index]
        self.scale = scaling
        self.animation_time = animation_duration
        super().__init__(game=game, path=self.path, scale=self.scale, animation_time=self.animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = hit_damage

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
