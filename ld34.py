

import sys
import pygame
import pyscroll

from collections import defaultdict
from pytmx.util_pygame import load_pygame

BLACK = (0, 0, 0)
GRID = 32


            # pygame.draw.rect(self.screen, (255, 255, 255), self.player)
        # self.player = pygame.Rect(200, 200, 32, 32)
        # self.gravity = 5
        # self.speed = [5, 5]

    # def update_player(self):
    #     self.player = self.player.move(self.speed)
    #
    #     if self.player.bottom > self.height:
    #         self.speed[1] = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.image = pygame.image.load('assets/player_start.png').convert()
        self.rect = self.image.get_rect()
        self._position = [200, 400]
        self.velocity = [400, 800]
        self.dead = False

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update(self, dt, obstacles):
        # Handle X position update
        self._position[0] += self.velocity[0] * dt
        self.rect.topleft = self._position

        # If we collide at this point with anything it means
        # we hit the side of the player. Unless it is the end
        # of the level that is a death.
        combined = obstacles['walls'] + obstacles['traps']
        collision_index = self.rect.collidelistall(combined)
        if len(collision_index) > 0:
            self.dead = True
            print 'DEATH!'
            return

        # Handle Y position update
        original_y = self._position[1]
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position

        # If we collide at this point with anything it means
        # we hit the top or bottom of the player. This could
        # be good or bad. Need to dig deeper!
        collision_index = self.rect.collidelistall(obstacles['walls'])
        if len(collision_index) > 0:
            self._position[1] = original_y
            self.rect.topleft = self._position

        collision_index = self.rect.collidelistall(obstacles['traps'])
        if len(collision_index) > 0:
            self.dead = True
            print 'DEATH!'


class LD34Game(object):
    def __init__(self):

        # PyGame Setup
        pygame.init()
        pygame.display.set_caption('Ludum Dare 34!!')

        self.screen_size = self.width, self.height = 1024, 640
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.fill(BLACK)

        # Gameplay Setup
        self.running = False
        self.player = Player()
        self.player_spawn = [200, 400]

        # Basic level setup
        self.obstacles = defaultdict(list)
        self.map_group = None

        self.load_level()

    def load_level(self):
        tmx_data = load_pygame('untitled.tmx')
        map_data = pyscroll.TiledMapData(tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, self.screen_size)

        for obj in tmx_data.objects:
            if 'gameType' in obj.properties:
                if obj.properties['gameType'] == 'wall':
                    self.obstacles['walls'].append(pygame.Rect(
                        obj.x, obj.y,
                        obj.width, obj.height
                    ))

                elif obj.properties['gameType'] == 'trap':
                    self.obstacles['traps'].append(pygame.Rect(
                        obj.x, obj.y,
                        obj.width, obj.height
                    ))

                elif obj.properties['gameType'] == 'spawn':
                    self.player_spawn = [obj.x, obj.y]

        self.map_group = pyscroll.PyscrollGroup(map_layer=map_layer)

        self.player.position = self.player_spawn
        self.map_group.add(self.player)

    def update(self, dt):
        self.map_group.update(dt, self.obstacles)

        if self.player.dead is True:
            self.reset_game()

    def reset_game(self):
        self.player.position = self.player_spawn
        self.player.dead = False

    def draw(self):
        x = self.player.rect.center[0]
        y = self.height / 2

        self.map_group.center((x, y))

        self.map_group.draw(self.screen)

    def run(self):
        clock = pygame.time.Clock()
        self.running = True

        try:
            while self.running is True:
                dt = clock.tick() / 1000.

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                self.update(dt)
                self.draw()

                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False


if __name__ == '__main__':
    try:
        LD34Game().run()
    except:
        pygame.quit()
        raise
