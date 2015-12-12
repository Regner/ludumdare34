

import sys
import pygame
import pyscroll
import logging

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
        self.velocity = [300, 300]

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update(self, dt, colliders):
        # Handle X position update
        self._position[0] += self.velocity[0] * dt
        self.rect.topleft = self._position

        # If we collide at this point with anything it means
        # we hit the side of the player. Unless it is the end
        # of the level that is a death.
        collision_index = self.rect.collidelistall(colliders)
        if len(collision_index) > 0:
            print 'You dun fucked up yo! Side impact!', colliders[collision_index]

        # Handle Y position update
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position

        # If we collide at this point with anything it means
        # we hit the top or bottom of the player. This could
        # be good or bad. Need to dig deeper!
        collision_index = self.rect.collidelistall(colliders)
        if len(collision_index) > 0:
            print 'Possible fuck up... collision on top or bot...', colliders[collision_index]




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

        # Basic level setup
        self.walls = []
        self.map_group = None

        self.load_level()

    def load_level(self):
        tmx_data = load_pygame('untitled.tmx')

        for obj in tmx_data.objects:
            self.walls.append(pygame.Rect(
                obj.x, obj.y,
                obj.width, obj.height
            ))

        map_data = pyscroll.TiledMapData(tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, self.screen_size)

        self.map_group = pyscroll.PyscrollGroup(map_layer=map_layer)

        self.player.position = map_layer.map_rect.center
        self.map_group.add(self.player)

    def update(self, dt):
        self.map_group.update(dt, self.walls)

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
