import pygame, os, sys, time
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

TIMER = 0
WHITE = (255, 255, 255)

def main():
    global cameraX, cameraY, TIMER
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Use arrows to move! Press space to shoot!")
    timer = pygame.time.Clock()

    intro_sequence = True
    game_play = True


    up = down = left = right = running = stationary = lstationary = melee = False
    imageint = 0

    bg = Surface((32,32))                               #creating a surface
    bg.convert()
    bg.fill((136,203,222))
    entities = pygame.sprite.Group()                        #making the entities group
    flame_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    flamethrower_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    cloud_group = pygame.sprite.Group()

                                                            #create enemies
    flamer1 = FlamethrowerEnemy(1000, 440, 930, 1200)
    flamer2 = FlamethrowerEnemy(3318, 345, 3094, 3574)
    flamer3 = FlamethrowerEnemy(1206, 720, 1038, 1574)
    flamer4 = FlamethrowerEnemy(3494, 720, 3302, 3702)
    flamer5 = FlamethrowerEnemy(4552, 720, 4232, 4952)
    flamer6 = FlamethrowerEnemy(4214, 160, 4118, 4302)
    flamer7 = FlamethrowerEnemy(2176, 600, 2096, 2240)
    flamer8 = FlamethrowerEnemy(5968, 250, 5872, 6008)

    cloud1 = Cloud(100, 100)
    cloud2 = Cloud(536, 200)
    cloud3 = Cloud(904, 150)
    cloud4 = Cloud(1650, 90)
    cloud5 = Cloud(2200, 110)
    cloud6 = Cloud(2600, 40)
    cloud7 = Cloud(3310, 150)
    cloud8 = Cloud(4000, 50)
    cloud9 = Cloud(4500, 100)
    cloud10 = Cloud(5600, 130)


    flamethrower_group.add(flamer1, flamer2, flamer3, flamer4, flamer5, flamer6, flamer7, flamer8)
    cloud_group.add(cloud1, cloud2, cloud3, cloud4, cloud5, cloud6, cloud7, cloud8, cloud9, cloud10)

    player = Player(50, 61)
    platforms = []

    x = y = 0                                               #creating the level
    level = [
        "                                                                                                                                                                                               B",
        "                                                                                                                                                                                               B",
        "                                                                                                                                                                                               B",
        "                                                                                                                                                             Gh                                B",
        "                                                                                                                                                             Bn                                B",
        "                                                                                                                                                Ggggh        Bn                                B",
        "                                                                                                                                                vjjjV        Bn                                B",
        "                                                                                           g                                     Gggggh                      Bn                                B",
        "                                                                                                                                 vjjjjV                      Bn                               EB",
        "                                                                               g                                                                             Bn                                B",
        "                                                                                                                                                             Bn                         Gggggh B",
        "                                                                                                                                                             Bn                         Jjjjjk B",
        "                                                                           Gh                    G              h                             Gggh           Bn                   G            B",
        "                                                                           Bn                    Bggggggggggggggn                             vjjV           Bn                   B            B",
        "                                                                           vV                    Bbjjjjjjjjjjjjbn             Gggggh                         Bn                   B            B",
        "                            G               h                                                    Bn            Bn             vjjjjV                         Bn            G      B            B",
        "                            Bgggggggggggggggn                                                    Bn            Bn                                            Bn            B      B            B",
        "Ggggh                       Bbbbbbbbbbbbbbbbn       g                           g                Bn            Bn                                            Bn            B      B            B",
        "Bbbbn                       vjjjjjjjjjjjjjjjV            Ggh                                     Bn            Bn           Gh                               Bn    Gh      B      B            B",
        "Bbbbn             Ggggh                                  Bbn                                     Bn            Bn          Gbn                               Bn    Bn      B      B            B",
        "Bbbbn            Gbbbbbh                                 Bbn                  g                  Bn    Ggggggggbn         Gbbn              Gggh             Bn    Bn      B      B            B",
        "Bbbbn            Bbbbbbn                                 Bbn      Ggggh                          Bn    Jjjjjjjjjk         Bbbn              vjjV             Jk    Bn      B      B            B",
        "Bbbbn            Bbbbbbn                                 Bbn      Bbbbn                          Bn                       Bbbn                                     Bn      B      B            B",
        "Bbbbn            Bbbbbbn                                 Bbn      Bbbbn                          Bn                       Bbbn                                     Bn      B      B           EB",
        "AbbbSQQQQQQQQQQQQAbbbbbSQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQAbSQQQQQQAbbbSQQQQQQQQQQQQQQQQQQQQQQQQQQAnQQQQQQQQQQQQQQQQQQQQQQQAbbSQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQASQQQQQQAQQQQQQAQQQQQQQQQQQQQ",]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)                             #add it to the group
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)                             #add it to the group
            if col == "G":                                  #grass brown edge left side
                g = Grass(x, y, 0, 32, 32, 32)
                platforms.append(g)
                entities.add(g)                             #add it to the group
            if col == "g":                                      #grass brown middle
                g = Grass(x, y, 32, 32, 32, 32)
                platforms.append(g)
                entities.add(g)
            if col == "h":                                  #grass top brown bottom
                g = Grass(x, y, 64, 32, 32, 32)
                platforms.append(g)
                entities.add(g)
            if col == "B":                                      #dark brown column left side
                g = Grass(x, y, 384, 0, 32, 32)
                platforms.append(g)
                entities.add(g)
            if col == "b":                                      #black square
                g = Grass(x, y, 544, 128, 32, 32)
                platforms.append(g)
                entities.add(g)
            if col == "n":                                          #dark brown column right side
                g = Grass(x, y, 416, 0, 32, 32)
                platforms.append(g)
                entities.add(g)
            if col == "v":
                g = Grass(x, y, 160, 352, 32, 32)                       #blunt v shape left side
                platforms.append(g)
                entities.add(g)
            if col == "V":
                g = Grass(x, y, 192, 352, 32, 32)                           # blunt v shape right side
                platforms.append(g)
                entities.add(g)
            if col == "J":
                g = Grass(x, y, 96, 256, 32, 32)  # brown rocky bottom left side
                platforms.append(g)
                entities.add(g)
            if col == "j":
                g = Grass(x, y, 128, 256, 32, 32)  # brown rocky bottom middle
                platforms.append(g)
                entities.add(g)
            if col == "k":
                g = Grass(x, y, 160, 256, 32, 32)  # brown rocky bottom right side
                platforms.append(g)
                entities.add(g)
            if col == "Q":
                g = noncollideGrass(x, y, 416, 384, 32, 32)  # bottom weeds
                # platforms.append(g)
                entities.add(g)
            if col == "A":
                g = Grass(x, y, 384, 224, 32, 32)  # brown rocky base left side
                platforms.append(g)
                entities.add(g)
            if col == "S":
                g = Grass(x, y, 416, 224, 32, 32)  # brown rocky base right side
                platforms.append(g)
                entities.add(g)



            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32                   #width is the first or zeroth component
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)          #camera object is created
    entities.add(player)                                                        #add player to the entity group

    def blink():
        if pygame.time.get_ticks() % 1000 < 500:
            return True
        else:
            return False

    while True:
        while intro_sequence:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    intro_sequence = False
                    # time.sleep(1)

            intro_background = pygame.image.load("Images/JungleBack.png").convert()
            intro_rect = intro_background.get_rect()

            title = Text("arial", 80, "COMMANDO", 640 / 2 - 298, 800 / 2 - 113, (255, 255, 255))

            screen.blit(intro_background, intro_rect)
            # screen.blit(title.image, title.rect)

            if blink():
                screen.blit(title.image, title.rect)

            # pygame.clock.tick(60)
            pygame.display.flip()
        while game_play:
            timer.tick(60)
            TIMER += 1

            for e in pygame.event.get():
                if e.type == QUIT: raise SystemExit, "QUIT"
                if e.type == KEYDOWN and e.key == K_ESCAPE:             #allows you to exit by pressing the escape button
                    raise SystemExit, "ESCAPE"
                if e.type == KEYDOWN and e.key == K_UP:                 #key board movement commands
                    up = True
                if e.type == KEYDOWN and e.key == K_DOWN:
                    down = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                    imageint = 1
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                    imageint = 0
                if e.type == KEYDOWN and e.key == K_1:
                    running = True
                if e.type == KEYUP and e.key == K_RIGHT:
                    stationary = True

                if e.type == KEYDOWN and e.key == K_TAB:
                    melee = True

                if e.type == KEYUP and e.key == K_LEFT:
                    lstationary = True

                                                                        #direction change


                if e.type == KEYUP and e.key == K_UP:                   #reset the movements and allow proper control
                    up = False
                if e.type == KEYUP and e.key == K_DOWN:
                    down = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False

            # draw background
            for y in range(32):
                for x in range(32):
                    screen.blit(bg, (x * 32, y * 32))                   #what does * do?

            camera.update(player)


            # update player, draw everything else
            player.update(up, down, left, right, running, stationary, lstationary, melee, imageint, platforms, bullet_group, flame_group, flamethrower_group)            #update the player
            bullet_group.update(platforms)
            flame_group.update(platforms)
            flamethrower_group.update(flame_group, bullet_group, explosion_group, platforms)
            explosion_group.update()
            for e in entities:
                screen.blit(e.image, camera.apply(e))                       #blit all entities, apply the camera method
            for b in bullet_group:
                screen.blit(b.image, camera.apply(b))
            for f in flamethrower_group:
                screen.blit(f.image, camera.apply(f))
            for f in flame_group:
                screen.blit(f.trueimage, camera.apply(f))
            for e in explosion_group:
                screen.blit(e.image, camera.apply(e))
                if TIMER % 40 == 0:
                    explosion_group.empty()
                # flame_group.empty()
            for c in cloud_group:
                screen.blit(c.image, camera.apply(c))
            pygame.display.update()
                                                            #PROGRESS
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Spritesheet():
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        return image

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        # self.image = pygame.image.load("Images/SEAL/basicstanding.png").convert_alpha()

        self.counter = 0
        self.rightrun = False
        self.leftrun = False
        self.jumping = False
        self.crouch = False
        self.knife = False

        self.images = []                                        #RUNNING
        self.images.append("Images/SEAL/runningframe1.png")
        self.images.append("Images/SEAL/runningframe2.png")
        self.images.append("Images/SEAL/runningframe3.png")
        self.images.append("Images/SEAL/runningframe4.png")
        self.images.append("Images/SEAL/runningframe5.png")
        self.images.append("Images/SEAL/runningframe6.png")
        self.index = 0
        self.fakeimage = self.images[self.index]

        self.image = pygame.image.load(self.fakeimage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 61))
                                                                        #jumping
        self.imagesj = []
        self.imagesj.append("Images/SEAL/jumpingframe1.png")
        self.imagesj.append("Images/SEAL/jumpingframe2.png")
        self.imagesj.append("Images/SEAL/jumpingframe3.png")
        self.imagesj.append("Images/SEAL/jumpingframe4.png")
        self.imagesj.append("Images/SEAL/jumpingframe5.png")
        self.indexj = 0
        self.fakeimagej = self.imagesj[self.indexj]
                                                                        #STAT JUMP
        self.imagessj = []
        self.imagessj.append("Images/SEAL/statjumpframe1.png")
        self.imagessj.append("Images/SEAL/statjumpframe2.png")
        self.indexsj = 0
        self.fakeimagesj = self.imagessj[self.indexsj]

                                                                        #melee
        self.imagelist_melee = []
        sprite_sheet_melee = Spritesheet("Images/Sprite Sheets/SEALSpriteSheet.jpg")
        self.imagelist_melee.append(sprite_sheet_melee.get_image(0, 94, 80, 94))
        self.imagelist_melee.append(sprite_sheet_melee.get_image(0, 188, 80, 94))
        self.imagelist_melee.append(sprite_sheet_melee.get_image(0, 282, 80, 94))
        self.imagelist_melee.append(sprite_sheet_melee.get_image(0, 376, 80, 94))
        self.index_m = 0
        self.fakeimage_melee = self.imagelist_melee[self.index_m]


        self.rect = self.image.get_rect()
        self.rect = self.rect.move(40, 40)
        self.health = 100

    def update(self, up, down, left, right, running, stationary, lstationary, melee, imageint, platforms, bullet_group, flame_group, flamethrower_group):
        if up:
            # only jump if on the ground
            if self.onGround:
                self.yvel -= 10

            if TIMER % 10 == 0:
                self.indexj += 1
                if self.indexj >= len(self.imagesj):
                    self.indexj = 0

            self.jumping = True

        if down:
            pass
            self.crouch = True
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8

            if TIMER % 4 == 0:
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.leftrun = True

        if right:
            self.xvel = 8
                                                        # running animation
            if TIMER % 4 == 0:
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.rightrun = True

        if stationary:
            self.image = pygame.image.load("Images/SEAL/basicstanding.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 61))


        if lstationary:
            self.image = pygame.image.load("Images/SEAL/basicstanding.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 61))
            self.image = pygame.transform.flip(self.image, True, False)

        if melee:
            self.knife = True

        if imageint == 0:
            self.image = pygame.image.load("Images/SEAL/basicstanding.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 61))

        if not (left or right) and self.jumping:                                                #STAT JUMP IS MESSED UP, FIX LATER
            if TIMER % 20 == 0:
                self.indexsj += 1
                if self.indexsj >= len(self.imagessj):
                    self.indexsj = 0
            if not right:
                self.fakeimagesj = self.imagessj[self.indexsj]
                self.image = pygame.image.load(self.fakeimagesj).convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 61))
            if not left:
                self.fakeimagesj = self.imagessj[self.indexsj]
                self.image = pygame.image.load(self.fakeimagesj).convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 61))
                self.image = pygame.transform.flip(self.image, True, False)

            self.jumping = False

        if self.rightrun and self.jumping:
            self.fakeimagej = self.imagesj[self.indexj]
            self.image = pygame.image.load(self.fakeimagej).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 61))
            self.rightrun = False
            self.jumping = False

        if self.leftrun and self.jumping:
            self.fakeimagej = self.imagesj[self.indexj]
            self.image = pygame.image.load(self.fakeimagej).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 61))
            self.image = pygame.transform.flip(self.image, True, False)
            self.leftrun = False
            self.jumping = False

        if self.rightrun and not self.jumping:
            self.fakeimage = self.images[self.index]
            self.image = pygame.image.load(self.fakeimage).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 61))
            self.rightrun = False

        if self.leftrun and not self.jumping:
            self.fakeimage = self.images[self.index]
            self.image = pygame.image.load(self.fakeimage).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 61))
            self.image = pygame.transform.flip(self.image, True, False)
            self.leftrun = False

        if self.knife:
            self.fakeimage_melee = self.imagelist_melee[self.index_m]
            if TIMER % 1 == 0:
                self.index_m += 1
                if self.index_m >= len(self.imagelist_melee):
                    self.index_m = 0
                self.image = self.imagelist_melee[self.index_m]
            self.knife = False

        # if self.crouch:
        #     self.image = pygame.image.load("Images/SEAL/crouchframe1.png").convert_alpha()
        #     self.image = pygame.transform.scale(self.image, (50, 61))
        #     if lstationary:
        #         self.image = pygame.transform.flip(self.image, True, False)
        #     self.crouch = False


        if not self.onGround:
                                                    # only accelerate with gravity if in the air
            self.yvel += 0.3
                                                    # max falling speed
            if self.yvel > 100: self.yvel = 100


        if not (left or right):
            self.xvel = 0

        self.rect.left += self.xvel                     # increment in x direction
        self.collide(self.xvel, 0, platforms)           # do x-axis collisions
        self.rect.top += self.yvel              # increment in y direction
        self.onGround = False              # assuming we're in the air
        self.collide(0, self.yvel, platforms)       # do y-axis collisions

        key = pygame.key.get_pressed()


        if imageint == 0:                                                                                       #BULLETS SPACE
            if key[pygame.K_SPACE] and TIMER % 10 == 0:
                self.attack = Bullet(self.rect.x+33, self.rect.centery-15, 20, 13, 5, False)
                bullet_group.add(self.attack)
        elif imageint == 1:
            if key[pygame.K_SPACE] and TIMER % 10 == 0:
                self.attack = Bullet(self.rect.x, self.rect.centery - 13, -20, 13, 5, True)
                bullet_group.add(self.attack)

        print (self.rect.x, self.rect.y)

        for f in flame_group:
            if pygame.sprite.collide_rect(self, f):
                self.health -= 5

        # print(self.health)

        if self.rect.y > 740:
            self.rect.y = 740
            self.onGround = True
            self.yvel = 0

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    # print "collide right"
                if xvel < 0:
                    self.rect.left = p.rect.right
                    # print "collide left"
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom


class Explosion(Entity):
    def __init__(self, xpos, ypos, width, height, xoff, yoff):
        Entity.__init__(self)
        self.imagelist = []
        sprite_sheet = Spritesheet("Images/Sprite Sheets/ExplosionSpriteSheet.png")
        self.imagelist.append(sprite_sheet.get_image(0, 130, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(130, 130, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(260, 130, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(390, 130, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(520, 130, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(650, 130, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(0, 260, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(130, 260, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(260, 260, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(390, 260, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(520, 260, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(650, 260, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(0, 390, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(130, 390, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(260, 390, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(390, 390, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(520, 390, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(650, 390, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(0, 520, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(130, 520, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(260, 520, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(390, 520, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(520, 520, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(650, 520, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(0, 650, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(130, 650, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(260, 650, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(390, 650, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(520, 650, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(650, 650, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(0, 780, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(130, 780, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(260, 780, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(390, 780, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(520, 780, 130, 130))
        self.imagelist.append(sprite_sheet.get_image(650, 780, 130, 130))

        self.index = 0

        self.image = self.imagelist[self.index]

        self.rect = self.image.get_rect()
        self.rect.x = xpos + xoff
        self.rect.y = ypos + yoff

    def update(self):
        if TIMER % 1 == 0:
            self.index += 1
            if self.index >= len(self.imagelist):
                self.index = 0
            self.image = self.imagelist[self.index]

        # self.trueimage = pygame.image.load(self.image)
        # self.trueimage = pygame.transform.scale(self.trueimage, (80, 40))
        # Entity.__init__(self)
        # sprite_sheet = Spritesheet("Images/Sprite Sheets/ExplosionSpriteSheet.png")
        # self.image = sprite_sheet.get_image(0, 130, 130, 130)
        # self.rect = self.image.get_rect()
        # self.rect.x = xpos + xoff
        # self.rect.y = ypos + yoff

class Flame(Entity):
    def  __init__(self, xpos, ypos, bulleth, bulletw, leftfacing):
        Entity.__init__(self)
        self.images = []
        self.images.append("Images/Flamethrower/stage1flame.gif")
        self.images.append("Images/Flamethrower/stage2flame.gif")
        self.images.append("Images/Flamethrower/stage3flame.gif")
        self.images.append("Images/Flamethrower/stage4flame.gif")
        self.index = 0
        self.image = self.images[self.index]
        self.leftflame = False
        if leftfacing:
            self.leftflame = True

        self.trueimage = pygame.image.load(self.image)
        self.trueimage = pygame.transform.scale(self.trueimage, (bulleth, bulletw))
        self.rect = self.trueimage.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

    def update(self, platforms):
        if TIMER % 2 == 0:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.trueimage = pygame.image.load(self.image)
            # self.trueimage = pygame.transform.scale(self.trueimage, (80, 40))                                 # NOT EXACTLY NEEDED UNLESS WE WANT ALL FLAMES TO BE THE SAME DIMENSIONS
            if self.leftflame:
                self.trueimage = pygame.transform.flip(self.trueimage, True, False)
                # self.leftflame = False

        if TIMER % 15 == 0:
            self.kill()

        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.kill()
                # if self.speed > 0:
                #     self.rect.right = p.rect.left
                #     self.kill()
                # if self.speed < 0:
                #     self.rect.x = p.rect.x
                #     self.kill()
        # if not self.leftflame:
        #     self.trueimage = pygame.image.load(self.image)
        #     self.trueimage = pygame.transform.scale(self.trueimage, (80, 40))
        #
        # if self.leftflame:
        #     self.trueimage = pygame.image.load(self.image)
        #     self.trueimage = pygame.transform.flip(self.trueimage, True, False)
        #     self.trueimage = pygame.transform.scale(self.trueimage, (80, 40))

class Bullet(Entity):
    def  __init__(self, xpos, ypos, posnegspeed, bulleth, bulletw, leftfacing):
        Entity.__init__(self)

        self.speed = posnegspeed

        self.image = pygame.image.load("Images/yellowbullet.png")
        self.image = pygame.transform.scale(self.image, (bulleth, bulletw))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

        self.leftbullet = False
        if leftfacing:
            self.leftbullet = True

    def update(self, platforms):
        if self.rect.x < 0 or self.rect.x > 6000:
            self.kill()
        self.rect.x += self.speed

        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.collide(self.speed, platforms)

    def collide(self, xvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if self.speed > 0:
                    self.rect.right = p.rect.left
                    self.kill()
                if self.speed < 0:
                    self.rect.x = p.rect.x
                    self.kill()

class FlamethrowerEnemy(Entity):
    def __init__(self, xpos, ypos, xmin, xmax):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/Flamethrower/basicflamer1.gif")
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.health = 100
        self.xvel = 0
        self.running = False

        self.imagelist_run = []
        sprite_sheet = Spritesheet("Images/Sprite Sheets/FlamethrowerSpriteSheet.gif")
        self.imagelist_run.append(sprite_sheet.get_image(0, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(51, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(104, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(156, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(208, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(260, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(312, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(364, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(416, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(468, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(520, 51, 48, 45))
        self.imagelist_run.append(sprite_sheet.get_image(572, 51, 48, 45))


        self.index = 0

        self.image = self.imagelist_run[self.index]

        self.xmin = xmin
        self.xmax = xmax
        self.delta = 3
        self.facing = "right"

    def update(self, flame_group, bullet_group, explosion_group, platforms):
        self.collide(self.xvel, 0, platforms)

        if self.rect.x > self.xmax:
            self.delta = -1
        if self.rect.x < self.xmin:
            self.delta = 1

        self.xvel = self.delta
        self.rect.x += self.xvel

        if TIMER % 5 == 0:
            self.index += 1
            if self.index >= len(self.imagelist_run):
                self.index = 0

            if self.delta > 0:
                # print("right")
                self.image = self.imagelist_run[self.index]
                self.image = pygame.transform.scale(self.image, (65, 70))
                self.image = pygame.transform.flip(self.image, True, False)

            elif self.delta < 0:
                # print"left"
                self.image = self.imagelist_run[self.index]
                self.image = pygame.transform.scale(self.image, (65, 70))

        if self.delta < 0:
            if TIMER % 8 == 0:
                self.flames = Flame(self.rect.x - 200, self.rect.y + 10, 10, 46, False)
                flame_group.add(self.flames)

        if self.delta > 0:
            if TIMER % 8 == 0:
                self.flames = Flame(self.rect.x + 80, self.rect.y + 10, 10, 46, True)
                flame_group.add(self.flames)

        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.health -= 10
            if self.health < 10:
                self.kill()
                self.boom = Explosion(self.rect.x, self.rect.y, 70, 60, -30, -40)
                explosion_group.add(self.boom)


    def collide(self, xvel, yvel, platforms):
        self.facing = "left"
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.delta = -1

                    # print "collide right"
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.delta = 1

                    # print "collide left"
                # if yvel > 0:
                #     self.rect.bottom = p.rect.top
                #     self.onGround = True
                #     self.yvel = 0
                # if yvel < 0:
                #     self.rect.top = p.rect.bottom

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))

class Grass(Platform):
    def __init__(self, x, y, x2, y2, w, h):
        Platform.__init__(self, x, y)
        sprite_sheet = Spritesheet("Images/Sprite Sheets/JungleSpriteSheet.png")
        self.image = sprite_sheet.get_image(x2, y2, w, h)

class Text():
    def __init__(self, font, size, text, xpos, ypos, color):
        self.font = pygame.font.SysFont(str(font), int(size))
        self.image = self.font.render(str(text), 1, color).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(xpos, ypos)

class Cloud(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/cloud.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

class noncollideGrass(Entity):
    def __init__(self, x, y, x2, y2, w, h):
        Entity.__init__(self)
        sprite_sheet = Spritesheet("Images/Sprite Sheets/JungleSpriteSheet.png")
        self.image = sprite_sheet.get_image(x2, y2, w, h)
        # self.image = Surface((32, 32))
        # # self.image.convert()
        # self.rect = Rect(x, y, 32, 32)
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, 32, 32)

if __name__ == "__main__":
    main()