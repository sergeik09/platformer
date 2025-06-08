import pygame as pg
import pytmx

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80
TILE_SCALE = 2

font = pg.font.Font('pixelfont.ttf', 70)


class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 2
        super(Portal, self).__init__()
        self.load_animations()
        self.current_image = 0
        self.image = self.animation[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.bottom = y * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_animations(self):
        tile_size = 64

        self.animation = []
        num_images = 8

        spritesheet = pg.image.load("map/Green Portal Sprite Sheet.png")

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            image = pg.transform.flip(image, True, False)
            self.animation.append(image)

    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.animation):
                self.current_image = 0

            self.image = self.animation[self.current_image]
            self.timer = pg.time.get_ticks()


class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y, layer=0):
        self._layer = layer
        super(Platform, self).__init__()

        self.image = pg.transform.scale_by(image, TILE_SCALE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        self._layer = 2
        super(Coin, self).__init__()
        self.load_animations()
        self.current_image = 0
        self.image = self.animation[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_animations(self):
        tile_size = 16

        self.animation = []
        num_images = 5

        spritesheet = pg.image.load("Coin_gems/MonedaD.png")

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.animation.append(image)

    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.animation):
                self.current_image = 0

            self.image = self.animation[self.current_image]
            self.timer = pg.time.get_ticks()


class Worm(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, pos):
        self._layer = 1

        super(Worm, self).__init__()

        self.load_animations()
        self.current_animation = self.walk_animation_left
        self.current_image = 0

        self.image = self.current_animation[self.current_image]

        self.timer = 0
        self.interval = 200
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos  # Начальное положение персонажа

        self.left_edge = self.rect.left - 16 * TILE_SCALE * 2
        self.right_edge = self.rect.right + 16 * TILE_SCALE * 2

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width
        self.map_height = map_height

        self.direction = "left"

    def load_animations(self):
        tile_size = 32

        self.walk_animation_left = []
        num_images = 3
        spritesheet = pg.image.load("Sprite Pack 5/4 - Squirmy Wormy/Movement_(32 x 32).png")

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.walk_animation_left.append(image)

        self.walk_animation_right = [
            pg.transform.flip(image, True, False)
            for image in self.walk_animation_left
        ]

    def update(self, platforms):

        if self.direction == "right":
            self.velocity_x = 1
            if self.rect.right >= self.right_edge:
                self.direction = "left"
                self.current_animation = self.walk_animation_left
        elif self.direction == "left":
            self.velocity_x = -1
            if self.rect.left <= self.left_edge:
                self.direction = "right"
                self.current_animation = self.walk_animation_right

        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right
                self.direction = 'right'
                self.current_animation = self.walk_animation_right
            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left
                self.direction = 'left'
                self.current_animation = self.walk_animation_left

        if pg.time.get_ticks() - self.timer > self.interval and not self.is_jumping:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()


class Croc(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, pos):
        self._layer = 1

        super(Croc, self).__init__()

        self.load_animations()
        self.current_animation = self.walk_animation_left
        self.current_image = 0

        self.image = self.current_animation[self.current_image]

        self.timer = 0
        self.interval = 200
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos  # Начальное положение персонажа

        self.left_edge = self.rect.left - 16 * TILE_SCALE * 3
        self.right_edge = self.rect.right + 16 * TILE_SCALE * 3

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width
        self.map_height = map_height

        self.direction = "left"

    def load_animations(self):
        tile_size = 32

        self.walk_animation_left = []
        num_images = 12
        spritesheet = pg.image.load("Sprite Pack 5/6 - Mr. Chomps/Crawl_&_Blink_(32 x 32).png")

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.walk_animation_left.append(image)

        self.walk_animation_right = [
            pg.transform.flip(image, True, False)
            for image in self.walk_animation_left
        ]

    def update(self, platforms):

        if self.direction == "right":
            self.velocity_x = 2
            if self.rect.right >= self.right_edge:
                self.direction = "left"
                self.current_animation = self.walk_animation_left
        elif self.direction == "left":
            self.velocity_x = -2
            if self.rect.left <= self.left_edge:
                self.direction = "right"
                self.current_animation = self.walk_animation_right

        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right
                self.direction = 'right'
                self.current_animation = self.walk_animation_right
            if platform.rect.collidepoint(self.rect.midright):
                self.direction = 'left'
                self.current_animation = self.walk_animation_left
                self.rect.right = platform.rect.left

        if pg.time.get_ticks() - self.timer > self.interval and not self.is_jumping:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()


class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Ball, self).__init__()

        self.direction = direction
        self.speed = 10
        self.interval = 10000
        self.image = pg.image.load('Sprite Pack 5/ball.png')
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()
        if direction == 'right':
            self.rect.x = player_rect.right
        else:
            self.rect.right = player_rect.left
        self.rect.y = player_rect.centery

    def update(self, left_edge, right_edge):
        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.right < left_edge or self.rect.x > right_edge:
            self.kill()


class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        self._layer = 1

        super(Player, self).__init__()

        self.load_animations()
        self.current_animation = self.idle_animation_right
        self.current_image = 0

        self.image = self.current_animation[self.current_image]

        self.timer = 0
        self.interval = 200
        self.rect = self.image.get_rect()
        self.rect.center = (200, 30)
        self.phys_body = pg.Rect(0, 0, self.rect.w // 2, self.rect.h)
        self.phys_body.midbottom = self.rect.midbottom
        # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width
        self.map_height = map_height

        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000

    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()

    def update(self, platforms):

        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()

        if keys[pg.K_a]:
            if self.current_animation != self.running_animation_left:
                self.current_animation = self.running_animation_left
                self.current_image = 0
            self.velocity_x = -6
        elif keys[pg.K_d]:
            if self.current_animation != self.running_animation_right:
                self.current_animation = self.running_animation_right
                self.current_image = 0
            self.velocity_x = 6
        else:
            if self.current_animation not in (
                    self.idle_animation_right, self.idle_animation_left
            ):
                if self.current_animation == self.running_animation_left:
                    self.current_animation = self.idle_animation_left
                elif self.current_animation == self.running_animation_right:
                    self.current_animation = self.idle_animation_right
            self.velocity_x = 0

        new_x = self.phys_body.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.phys_body.width:
            self.phys_body.x = new_x

        self.velocity_y += self.gravity
        if self.velocity_y > 16 * TILE_SCALE:
            self.velocity_y = 16 * TILE_SCALE
        self.phys_body.y += self.velocity_y
        self.rect.midbottom = self.phys_body.midbottom

        for platform in platforms:
            if platform.rect.collidepoint(self.phys_body.midbottom):
                self.phys_body.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            if platform.rect.collidepoint(self.phys_body.midtop):
                self.phys_body.top = platform.rect.bottom
                self.velocity_y = 0

            if platform.rect.collidepoint(self.phys_body.midleft):
                self.phys_body.left = platform.rect.right
            if platform.rect.collidepoint(self.phys_body.midright):
                self.phys_body.right = platform.rect.left

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0

            if not self.is_jumping or self.velocity_y > 0:
                self.image = self.current_animation[self.current_image]
            else:
                self.image = self.jumping_animation[self.velocity_x < 0]

            self.timer = pg.time.get_ticks()

        # if self.is_jumping or self.velocity_y < 0:
        #     self.image = self.current_animation[self.current_image]
        # elif self.velocity_y >0:
        #     self.current_animation = self.falling_animation_left if self.velocity_x < 0 else self.falling_animation_right

    def load_animations(self):
        tile_size = 32

        self.idle_animation_right = []
        num_images = 5

        spritesheet = pg.image.load("Sprite Pack 5/2 - Lil Wiz/Idle_(32 x 32).png")

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.idle_animation_right.append(image)

        self.idle_animation_left = [pg.transform.flip(image, True, False)
                                    for image in self.idle_animation_right]

        self.running_animation_right = []
        num_images = 6

        spritesheet = pg.image.load("Sprite Pack 5/2 - Lil Wiz/Running_(32 x 32).png")

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.running_animation_right.append(image)

        self.running_animation_left = [
            pg.transform.flip(image, True, False)
            for image in self.running_animation_right
        ]

        self.falling_animation_right = []
        num_images = 2

        spritesheet = pg.image.load("Sprite Pack 5/2 - Lil Wiz/Falling_(32 x 32).png")

        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)
            self.falling_animation_right.append(image)

        self.falling_animation_left = [
            pg.transform.flip(image, True, False)
            for image in self.falling_animation_right
        ]

        self.jumping_animation = []

        image = pg.image.load("Sprite Pack 5/2 - Lil Wiz/Jumping_(32 x 32).png")

        image = pg.transform.scale_by(image, TILE_SCALE)
        left_image = pg.transform.flip(image, True, False)
        self.jumping_animation.append(image)
        self.jumping_animation.append(left_image)
        # self.
        # image = pg.image.load("Sprite Pack 5/2 - Lil Wiz/Falling_(32 x 32).png")
        #
        # image = pg.transform.scale_by(image, TILE_SCALE)
        # left_image = pg.transform.flip(image, True, False)
        # self.jumping_animation[1].append(image)
        # self.jumping_animation[1].append(left_image)

    def jump(self):
        self.velocity_y = -TILE_SCALE * 19
        self.is_jumping = True


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.level = 1
        self.setup()

    # noinspection PyAttributeOutsideInit
    def setup(self):
        pg.mixer.init()
        pg.mixer.music.load('music/JRPG_mainTheme.ogg')
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play()
        self.coin_sound = pg.mixer.Sound('sounds/coin.flac')
        self.coin_sound.set_volume(0.1)
        self.clock = pg.time.Clock()
        self.is_running = False
        self.mode = 'game'
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.collected_coins = 0

        self.sky = pg.image.load("map/sky.png")
        self.mountains = pg.image.load("map/mountains.png")
        self.ruins = pg.image.load("map/ruins.png")

        sky_scale = SCREEN_HEIGHT / self.sky.get_height()
        mountains_scale = SCREEN_HEIGHT / self.mountains.get_height()
        ruins_scale = SCREEN_HEIGHT / self.ruins.get_height()

        self.sky = pg.transform.scale(self.sky,
                                      (int(self.sky.get_width() * sky_scale), SCREEN_HEIGHT))
        self.mountains = pg.transform.scale(self.mountains,
                                            (int(self.mountains.get_width() * mountains_scale), SCREEN_HEIGHT))
        self.ruins = pg.transform.scale(self.ruins,
                                        (int(self.ruins.get_width() * ruins_scale), SCREEN_HEIGHT))

        self.tmx_map = pytmx.load_pygame(f"map/level {self.level}.tmx")

        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE

        self.player = Player(self.map_pixel_width, self.map_pixel_height)

        self.all_sprites.add(self.player)

        for layer in self.tmx_map:
            for x, y, gid in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)

                if tile:
                    if layer.name == "platforms":
                        platform = Platform(
                            tile,
                            x * self.tmx_map.tilewidth,
                            y * self.tmx_map.tileheight,
                            layer=1
                        )
                        self.all_sprites.add(platform)
                        self.platforms.add(platform)

                    elif layer.name == 'portals':
                        portal = Portal(
                            x * self.tmx_map.tilewidth,
                            y * self.tmx_map.tileheight,
                        )
                        self.all_sprites.add(portal)
                        self.portals.add(portal)

                    elif layer.name == 'foreground':
                        platform = Platform(
                            tile,
                            x * self.tmx_map.tilewidth,
                            y * self.tmx_map.tileheight,
                            layer=2
                        )
                        self.all_sprites.add(platform)

                    elif layer.name == "worms":
                        worm = Worm(self.map_pixel_width, self.map_pixel_height,
                                    (x * self.tmx_map.tilewidth * TILE_SCALE,
                                     y * self.tmx_map.tileheight * TILE_SCALE)
                                    )
                        self.all_sprites.add(worm)
                        self.enemies.add(worm)

                    elif layer.name == 'coins':
                        coin = Coin(x * self.tmx_map.tilewidth,
                                    y * self.tmx_map.tileheight)

                        self.coins.add(coin)
                        self.all_sprites.add(coin)

                    elif layer.name == "crocodiles":
                        croc = Croc(self.map_pixel_width, self.map_pixel_height,
                                    (x * self.tmx_map.tilewidth * TILE_SCALE,
                                     y * self.tmx_map.tileheight * TILE_SCALE)
                                    )
                        self.all_sprites.add(croc)
                        self.enemies.add(croc)

                    else:
                        platform = Platform(
                            tile,
                            x * self.tmx_map.tilewidth,
                            y * self.tmx_map.tileheight
                        )
                        self.all_sprites.add(platform)

        self.coins_amount = len(self.coins.sprites())

        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4

        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                direction = 'right' if self.player.current_animation in (
                    self.player.idle_animation_right, self.player.running_animation_right) else 'left'
                ball = Ball(self.player.rect, direction)
                self.balls.add(ball)
                self.all_sprites.add(ball)
            if self.mode == "game over":
                if event.type == pg.KEYDOWN:
                    self.setup()

        keys = pg.key.get_pressed()

        # if keys[pg.K_LEFT]:
        #     self.camera_x += self.camera_speed
        # if keys[pg.K_RIGHT]:
        #     self.camera_x -= self.camera_speed
        # if keys[pg.K_UP]:
        #     self.camera_y += self.camera_speed
        # if keys[pg.K_DOWN]:
        #     self.camera_y -= self.camera_speed

    def update(self):
        if self.player.hp <= 0:
            self.mode = "game over"
            return

        if self.player.rect.y >= self.map_pixel_height:
            self.player.hp = 0

        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()

        self.player.update(self.platforms)
        self.enemies.update(self.platforms)
        self.balls.update(self.player.rect.x - SCREEN_WIDTH // 2,
                          self.player.rect.x + SCREEN_WIDTH // 2)
        self.coins.update()
        self.portals.update()
        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2

        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))

        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))

        pg.sprite.groupcollide(self.balls, self.enemies, True, True)

        pg.sprite.groupcollide(self.balls, self.platforms, True, False)

        if pg.sprite.spritecollide(self.player, self.portals, False) and self.collected_coins > self.coins_amount /2:
            self.level += 1
            self.setup()

        hits = pg.sprite.spritecollide(self.player, self.coins, True)

        for hit in hits:
            self.collected_coins += 1
            self.coin_sound.play()

    def draw(self):
        for i in range(-1, (SCREEN_WIDTH // self.sky.get_width()) + 2):
            self.screen.blit(self.sky, (i * self.sky.get_width(), 0))

        mountains_offset = -(self.camera_x * 0.2) % self.mountains.get_width()
        for i in range(-1, (SCREEN_WIDTH // self.mountains.get_width()) + 2):
            self.screen.blit(self.mountains,
                             (mountains_offset + i * self.mountains.get_width(), 65 - self.camera_y * 0.2))

        ruins_offset = -(self.camera_x * 0.4) % self.ruins.get_width()
        for i in range(-1, (SCREEN_WIDTH // self.ruins.get_width()) + 2):
            self.screen.blit(self.ruins, (ruins_offset + i * self.ruins.get_width(), 265 - self.camera_y * 0.4))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))

        # pg.draw.rect(self.screen, pg.Color("yellow"), self.player.rect.move(-self.camera_x, -self.camera_y), 4)
        # pg.draw.rect(self.screen, pg.Color("red"), self.player.phys_body.move(-self.camera_x, -self.camera_y), 4)
        pg.draw.rect(self.screen, pg.Color(255, int(self.player.hp / 10 * 255), 0), (20, 20, self.player.hp * 10, 15))
        pg.draw.rect(self.screen, pg.Color("black"), (20, 20, 100, 15), 2)

        self.screen.blit(font.render(f'{self.cfollected_coins}', False, pg.Color('yellow')), (SCREEN_WIDTH - 50, 20))

        if self.mode == 'game over':
            text = font.render("Game  Over", False, (255, 0, 0))

            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
        pg.display.flip()


if __name__ == "__main__":
    game = Game()
