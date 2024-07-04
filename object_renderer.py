import pygame as pg

from map import map_index
from settings import *
import weapon
from weapon import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        #self.end_image = self.get_texture('resources/textures/End.png', [908, 376])

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_player_ammo()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))
        print(map_index)

    #def end(self):
        #self.screen.blit(self.end_image, (200, 200))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def draw_player_ammo(self):
        rocket_launcher = str(weapon.rocket_launcher_ammo)
        shotgun = str(weapon.shotgun_ammo)
        super_shotgun = str(weapon.super_shotgun_ammo)
        golden_gun = str(weapon.golden_gun_ammo)
        if(rocket_launcher<='0'):
            rocket_launcher='0'
        elif(shotgun<= '0'):
            shotgun='0'
        elif (super_shotgun <= '0'):
            super_shotgun = '0'
        elif (golden_gun <= '0'):
            golden_gun = '0'
        if(weapon.weapon_index==0):
            for i, char in enumerate(shotgun):
                self.screen.blit(self.digits[char], (i * self.digit_size, 100))
        if (weapon.weapon_index == 1):
            for i, char in enumerate(super_shotgun):
                self.screen.blit(self.digits[char], (i * self.digit_size, 100))
        if (weapon.weapon_index == 2):
            for i, char in enumerate(golden_gun):
                self.screen.blit(self.digits[char], (i * self.digit_size, 100))



    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }