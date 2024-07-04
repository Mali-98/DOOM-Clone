from settings import *
import pygame as pg
import math
import map
from map import *
health_recovery_delay=700
import weapon
from weapon import *
class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = health_recovery_delay
        self.time_prev = pg.time.get_ticks()
        # diagonal movement correction
        self.diag_move_corr = 1 / math.sqrt(2)

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1
            if (weapon.weapon_index==0 and weapon.shotgun_ammo<=99):
                weapon.shotgun_ammo += 1
            elif(weapon.weapon_index==1 and weapon.super_shotgun_ammo<=49):
                weapon.super_shotgun_ammo += 1
            elif(weapon.weapon_index==2 and weapon.golden_gun_ammo<=24):
                weapon.golden_gun_ammo += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:

                if ((weapon.weapon_index == 2 and weapon.golden_gun_ammo <= 0) or (weapon.weapon_index == 0 and weapon.shotgun_ammo <= 0) or (weapon.weapon_index == 1 and weapon.super_shotgun_ammo <= 0)):
                    pass
                else:
                    self.game.sound.shotgun.play()
                    self.shot = True
                    self.game.weapon.reloading = True
                if(weapon.weapon_index==2):
                    weapon.golden_gun_ammo-=1
                elif(weapon.weapon_index==0):
                    weapon.shotgun_ammo-=1
                elif (weapon.weapon_index == 1):
                    weapon.super_shotgun_ammo -= 1

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos
        #if keys[pg.K_h]:
            #map.map_index += 4
            #self.game.new_game()
        if keys[pg.K_1]:
            weapon.weapon_index = 0
            weapon.scaling = 0.6
            weapon.animation_duration = 100
            weapon.hit_damage = 100
            self.game.weapon_functions()
        if keys[pg.K_2]:
            weapon.weapon_index = 1
            weapon.scaling = 0.6
            weapon.animation_duration = 120
            weapon.hit_damage = 200
            self.game.weapon_functions()
        if keys[pg.K_3]:
            weapon.weapon_index = 2
            weapon.scaling = 0.4
            weapon.animation_duration = 100
            weapon.hit_damage = 500
            self.game.weapon_functions()


        # diag move correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()
        #self.recover_ammo()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)